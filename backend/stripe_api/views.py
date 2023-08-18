import stripe
from stripe.error import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from .serializers import *
from api.pay import PayClass
from rest_framework.views import APIView
from .models import Card
stripe.api_key = 'sk_test_51LsYgMIm06Z4dmHxYoYxl1NfwANfvRmTAuDUTJT4SWueF62xPD8r5lYNunduruEmLpO6XcHOVRLpy2qx8WpW2gwj00kcLeYU9z'
#Card to Momo Transaction
class StripeCharge(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = StripeSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data["amount"]
        currency = "USD"
        phone_number = serializer.validated_data['phone_number']
        card_token = serializer.validated_data['card_token']  # Token obtained from secure card form
        txt_ref = "Card-to-momo transaction"

        stripe.api_key = 'sk_test_51LsYgMIm06Z4dmHxYoYxl1NfwANfvRmTAuDUTJT4SWueF62xPD8r5lYNunduruEmLpO6XcHOVRLpy2qx8WpW2gwj00kcLeYU9z'
        
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency=currency,
                source=card_token,
                description='Card to Momo Transfer'
            )
            
            # Assuming the charge was successful, proceed with verification and Momo withdrawal
            charge_id=charge.id
            verified = self.verify_stripe_charge(charge_id)
            if verified:
                currency = "EUR"
                response_data = PayClass.withdrawmtnmomo(amount, currency, txt_ref, phone_number, payermessage="Sent from card")
                txt_ref = response_data['ref']
                response_data = PayClass.checkwithdrawstatus(txt_ref)

                return Response({"message": "Money Sent Successfully"})
            else:
                return Response({"message": "There was an error"},status=400)
            
        except StripeError as e:
            return Response({"error": str(e)}, status=500)
        
        
        
    def verify_stripe_charge(self, charge_id):
        try:
            charge = stripe.Charge.retrieve(charge_id)
            
            # Check if the charge was successful
            if charge.paid and charge.status == "succeeded":
                return True
            else:
                return False
        except StripeError as e:
            raise ValueError(str(e))
        





#Virtual Card Aquisition and top-up with MTN momo
class CreateCustomerView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = CustomerFormSerializer
    def post(self, request, format=None):
        serializer = CustomerFormSerializer(data=request.data)
        
        if serializer.is_valid():
            form_data = serializer.validated_data
            
            customer = stripe.issuing.Cardholder.create(
                name=str(form_data['first_name']+form_data['last_name']),
                email=request.user.email,
                phone_number=form_data['phone'],
                status="active",
                type="individual",
                individual={
                    "first_name": form_data['first_name'],
                    "last_name": form_data['last_name'],
                    "dob": {"day": 1, "month": 11, "year": 1981},
                },
                billing={
                    "address": {
                        "line1": form_data['address_line'],
                        "city": form_data['town'],
                        "state": "CA",
                        "postal_code": "00233",
                        "country": "US",
                    },
                },
            )
            
            Card.objects.create(user=request.user, customer_id=customer.id)
            
            return Response({"message": "Customer created successfully"})
        else:
            return Response({"message": "Problem with form"}, status=400)

class CreateCardView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def get(self, request, format=None):
        user = request.user
        try:
            card = Card.objects.get(user=user)
            create = stripe.issuing.Card.create(
                currency='usd',
                type='virtual',
                cardholder=card.customer_id
            )
            card.card_id = create.id
            retrieve = stripe.issuing.Card.retrieve(create.id)
            card_number = str(400000999000)
            card.card_number = card_number + str(retrieve.last4)
            card.exp_month = retrieve.exp_month
            card.exp_year = retrieve.exp_year
            card.save()
        
            serializer = CardSerializer(card)
            return Response(serializer.data)
        except Card.DoesNotExist:
            return Response({"message":"User does not have a card"}, status=400)

class TopUpCardView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = TopupSerializer
    def post(self, request, format=None):
        serializer = TopupSerializer(data=request.data)
        
        if serializer.is_valid():
            form_data = serializer.validated_data
            top_up = stripe.Topup.create(
                destination_balance='issuing',
                amount=2000,
                currency='usd',
                description="Top-up for Issuing, August 18, 2023",
                statement_descriptor='Top-up',
            )
            
            # Retrieve the balance object
            balance = stripe.Balance.retrieve()
            
            # Extract the available Issuing balance in USD
            issuing_balance = next((bal for bal in balance.issuing.available if bal.currency == 'usd'), None)
            
            return Response({
                'issuing_balance': issuing_balance.amount if issuing_balance else 0
            })
        else:
            return Response({"message":"Invalid Form"},status=400)

class GetCardDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def get(self, request, format=None):
        card = Card.objects.get(user=request.user)
        serializer = CardSerializer(card)
        return Response(serializer.data)

