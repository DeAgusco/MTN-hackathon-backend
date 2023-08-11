from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to="media/user_profiles", blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'user-profile-for-{self.user.username}'