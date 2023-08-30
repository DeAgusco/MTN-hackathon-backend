# views.py
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(username=request.data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            response.data['token'] = token.key
        return response

class ObtainTokenView(ObtainAuthToken):
    def get(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = self.user
            token, _ = Token.objects.get_or_create(user=user)
            response.data['token'] = token.key
        return response
