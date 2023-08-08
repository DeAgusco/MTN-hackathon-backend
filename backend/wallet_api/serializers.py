from rest_framework import serializers
from .models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('user','balance', 'reference')  # List the fields you want to include in the serialized data

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('user','transaction_type','timestamp','amount')
        

class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.CharField(max_length=20)
    currency = serializers.CharField(max_length=3)
    phone_number = serializers.CharField(max_length=20)
    txt_ref = serializers.CharField(max_length=30)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['amount'] = str(data['amount'])  # Convert Decimal to string
        return data
    
class TransferSerializer(serializers.Serializer):
    amount = serializers.CharField(max_length=20)
    reciever = serializers.CharField(max_length =250)
