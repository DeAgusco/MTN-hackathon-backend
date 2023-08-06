from django.urls import path
from . import views

urlpatterns = [
    path('momo/pay/', views.momo_pay, name='momo-pay'),
    path('momo/verify/<str:txn>/', views.verify_momo_transaction, name='verify-momo-transaction'),
    path('momo/balance/', views.momo_balance, name='momo-balance'),
    path('momo/user-info/<str:account_holder_msisdn>/', views.get_basic_user_info, name='get-basic-user-info'),
]
