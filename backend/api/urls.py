from django.urls import path
from . import views

urlpatterns = [
    path('momo/pay/', views.momo_pay, name='momo-pay'),
    path('token/', views.get_user_token, name='get_user_token'),
    path('momo/verify/<str:txn>/', views.verify_momo_transaction, name='verify-momo-transaction'),
    path('momo/balance/', views.momo_balance, name='momo-balance'),
    path('momo/user-info/<str:account_holder_msisdn>/', views.get_basic_user_info, name='get-basic-user-info'),
    path('momo/withdraw/', views.initiate_withdrawal, name='initiate-withdrawal'),
    path('momo/disburse/', views.MoMoDisbursementView.as_view(), name='momo-disburse'),
    path('momo/disburse/status/<str:reference_id>/', views.MoMoDisbursementStatusView.as_view(), name='momo-disburse-status'),
]
