# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('obtain-token/', ObtainTokenView.as_view(), name='obtain-token'),
    # ... other patterns ...
]
