from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_mode = models.CharField(max_length=100, default='insightful')  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

def get_profile(self):
    return UserProfile.objects.get_or_create(user=self)[0]

User.add_to_class("profile", property(get_profile))
