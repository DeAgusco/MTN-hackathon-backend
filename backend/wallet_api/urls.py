from django.urls import path
from . import views

urlpatterns = [
    path('topup/', views.TopUpView.as_view(), name="top_up"),
    path('withdraw/', views.WithdrawalView.as_view(), name="withdraw"),
    path('transfer/initiate/', views.TransferFromWalletView.as_view(), name="transfer"),
    path('transfer/verify/', views.VerificationView.as_view(), name="verify_transfer"),
    path('transfer/reverse/', views.ReversalView.as_view(), name="reverse_transfer"),
    path('', views.WalletDetailView.as_view(), name='wallet-detail'),
    path('transactions/', views.TransactionListView.as_view(), name='wallet-detail'),
]
