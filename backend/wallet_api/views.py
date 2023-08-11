from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from api.pay import PayClass
from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer,TransactionSerializer,WithdrawalSerializer,TransferSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from account.models import UserProfile
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from channels.db import database_sync_to_async
#Basic functions
@receiver(user_logged_in)
@database_sync_to_async
def retrieve_offline_messages(sender, request, user, **kwargs):
    offline_messages = OfflineMessage.objects.filter(recipient=user)
    print("triggered")
    channel_layer = get_channel_layer()

    for message in offline_messages:
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}_group",
            {
                "type": "offline_message",
                "message": message.message,
                "timestamp": str(message.timestamp)
            }
        )
        message.delete()

def is_user_online(user_id):
    user = User.objects.get(id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile = UserProfile.objects.filter(user_id=user_id, is_online=True).first()
    if user_profile:
        return True
    else:
        return False
    
def send_offline_message(sender, recipient, message):
    offline_message = OfflineMessage.objects.create(
        sender=sender,
        recipient=recipient,
        message=message,
        timestamp=timezone.now()
    )


class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get_object(self):
        user_wallet = Wallet.objects.get(user=self.request.user)
        return user_wallet   
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get_queryset(self):
        user_transactions = Transaction.objects.filter(user=self.request.user)
        return user_transactions
class TopUpView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    
    def post(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
            response_data = self.momo_pay(request)
            reference = response_data['ref']
            print(reference)
            wallet.reference = reference
            wallet.save()
        except Wallet.DoesNotExist:
            response_data = self.momo_pay(request)
            reference = response_data.get('ref')
            wallet = Wallet.objects.create(user=request.user, reference=reference)

        # Verify Momo transaction
        wallet = Wallet.objects.get(user=request.user)
        txn = wallet.reference
        verification = self.verify_momo_transaction(txn)
        verified_amount = verification['amount']

        # Update wallet balance and save
        wallet.balance += int(verified_amount)
        wallet.save()

        # Create transaction record
        transaction = Transaction.objects.create(
            user=request.user,
            transaction_type='top_up',
            amount=verified_amount
        )
        transaction.save()

        return Response({'message': 'Wallet topped up successfully'})

    def verify_momo_transaction(self, txn):
        response_data = PayClass.verifymomo(txn)
        return response_data
    
    def momo_pay(self, request):
        amount = request.data.get("amount")
        currency = request.data.get("currency")
        txt_ref = request.data.get("txt_ref")
        phone_number = request.data.get("phone_number")
        payer_message = request.data.get("payer_message")
    
        response_data = PayClass.momopay(amount, currency, txt_ref, phone_number, payer_message)

        return response_data


class WithdrawalView(generics.CreateAPIView):
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_wallet = Wallet.objects.get(user=request.user)

        # Extract data from serializer
        amount = serializer.validated_data['amount']
        currency = serializer.validated_data['currency']
        phone_number = serializer.validated_data['phone_number']
        txt_ref = serializer.validated_data['txt_ref']

        if user_wallet.balance >= int(amount):
            response_data = PayClass.request_to_transfer(amount, currency, txt_ref, phone_number)
            reference_id = response_data['ref']
            response_data = PayClass.check_disbursement_status(reference_id)

            withdrawal_amount = response_data['amount']  # Store the withdrawal amount for response

            user_wallet.balance -= int(withdrawal_amount)
            user_wallet.save()

            # Create a Transaction record
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='withdrawal',
                amount=withdrawal_amount
            )
            transaction.save()

            return Response({"message": "Withdrawal successful"})
        else:
            return Response({"message": "Insufficient balance"},status=400)
#Inter Wallet Transfer with real-time updates on both ends
class TransferFromWalletView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    serializer_class = TransferSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract data from serializer
        amount = serializer.validated_data['amount']
        receiver_username = serializer.validated_data['reciever']
        receiver = User.objects.get(username=receiver_username)
        sender_wallet = Wallet.objects.get(user=request.user)
        sender_wallet.balance -= int(amount)
        sender_wallet.save()
        # Create transaction record
        transaction = Transaction.objects.create(
            user=request.user,
            transaction_type=f'Transfer to {receiver_username}',
            amount=amount
        )
        transaction.save()
        # Notify sender and receiver about transaction initiation
        sender_channel_layer = get_channel_layer()
        receiver_channel_layer = get_channel_layer()

        async_to_sync(sender_channel_layer.group_send)(
            f"user_{request.user.id}_group",
            {"type": "transaction.initiation"}
        )
        async_to_sync(receiver_channel_layer.group_send)(
            f"user_{receiver.id}_group",
            {"type": "transaction.initiation"}
        )
        if is_user_online(user_id=receiver.id):
            pass
        else:
            send_offline_message(sender=request.user, recipient=receiver, message='Transaction initiated')

        return Response({"message": "Transfer initiated"})
    
    def send_verification_notification(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract data from serializer
        amount = serializer.validated_data['amount']
        username = serializer.validated_data['reciever']
        receiver = User.objects.get(username=username)
        receiver_wallet, created = Wallet.objects.get_or_create(user=receiver)
        receiver_wallet.balance += int(amount)
        receiver_wallet.save()
        transaction = Transaction.objects.create(
            user=receiver,
            transaction_type=f'Money_Received',
            amount=amount
        )
        transaction.save()
        # Notify sender and receiver about transaction verification
        sender_channel_layer = get_channel_layer()
        receiver_channel_layer = get_channel_layer()

        async_to_sync(sender_channel_layer.group_send)(
            f"user_{request.user.id}_group",
            {"type": "transaction.verification"}
        )
        async_to_sync(receiver_channel_layer.group_send)(
            f"user_{receiver.id}_group",
            {"type": "transaction.verification"}
        )
        if is_user_online(user_id=receiver.id):
            pass
        else:
            send_offline_message(sender=request.user, recipient=receiver, message='Transaction Verified')
        
    def send_reversal_notification(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract data from serializer
        amount = serializer.validated_data['amount']
        username = serializer.validated_data['reciever']
        receiver = User.objects.get(username=username)
        receiver_wallet = Wallet.objects.get(user=request.user)
        receiver_wallet.balance += int(amount)
        receiver_wallet.save()
        transaction = Transaction.objects.create(
            user=receiver,
            transaction_type=f'Money_Reversed',
            amount=amount
        )
        transaction.save()
        # Notify sender and receiver about transaction verification
        sender_channel_layer = get_channel_layer()
        receiver_channel_layer = get_channel_layer()

        async_to_sync(sender_channel_layer.group_send)(
            f"user_{request.user.id}_group",
            {"type": "transaction.reversal"}
        )
        async_to_sync(receiver_channel_layer.group_send)(
            f"user_{receiver.id}_group",
            {"type": "transaction.reversal"}
        )
        if is_user_online(user_id=receiver.id):
            pass
        else:
            send_offline_message(sender=request.user, recipient=receiver, message='Transaction Reversed')
        
class VerificationView(TransferFromWalletView):
    
    def create(self, request, *args, **kwargs):
        self.send_verification_notification(request)
        return Response({"message": "Verification notification sent"})
    
class ReversalView(TransferFromWalletView):
    
    def create(self, request):
        self.send_reversal_notification(request)
        return Response({"message": "Reversal notification sent"})
    