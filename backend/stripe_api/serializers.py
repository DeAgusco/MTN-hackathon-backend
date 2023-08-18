from rest_framework import serializers

from .models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CustomerFormSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    town = serializers.CharField()
    address_line = serializers.CharField()
    phone = serializers.CharField()
    # ... other fields ...

class StripeSerializer(serializers.Serializer):
    amount = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length =250)
    card_token = serializers.CharField(max_length =250)
    
class TopupSerializer(serializers.Serializer):
    amount = serializers.CharField()
    phone = serializers.CharField()