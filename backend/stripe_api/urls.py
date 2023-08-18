from django.urls import path
from .import views
urlpatterns = [
    path("charge/", views.StripeCharge.as_view(),name="stripe_initiate"),
    path('create-customer/', views.CreateCustomerView.as_view(), name='create-customer'),
    path('create-card/', views.CreateCardView.as_view(), name='create-card'),
    path('top-up-card/', views.TopUpCardView.as_view(), name='top-up-card'),
    path('get-card-details/', views.GetCardDetailsView.as_view(), name='get-card-details'),
]
