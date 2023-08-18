from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference = models.CharField(max_length=290,blank=True, null=True)
    def __str__(self):
        return f'{self.user.username}-wallet-with-balance: {self.balance}'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)  # 'deposit', 'withdraw', etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=250, blank=True, null=True)
    def __str__(self):
        return f'{self.user.username}-wallet-with-balance: {self.transaction_type}'
    


class OfflineMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offline_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.message}-for-{self.recipient}-from-{self.sender}'
    

