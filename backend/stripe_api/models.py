from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Card(models.Model):
    user = models.ForeignKey(User, verbose_name=("user"), on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=250)
    card_id = models.CharField(max_length=250, blank=True, null=True)
    card_number = models.CharField(max_length=50, blank=True, null=True)
    exp_month = models.CharField(max_length=2, blank=True, null=True)
    exp_year = models.CharField(max_length=2,blank=True, null=True)
    cvc = models.CharField(default=123, max_length=3)
    def __str__(self):
        return f'{self.user.username}-has card {self.card_id}'