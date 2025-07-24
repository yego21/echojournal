from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz
from journal.models import JournalMode

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_mode = models.ForeignKey(
        'journal.JournalMode',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(
        max_length=100,
        choices=[(tz, tz) for tz in pytz.all_timezones],
        default='UTC',
        blank=True,
        null=True,
    )
    selected_mode = models.ForeignKey(
        JournalMode, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='users'
    )

    def __str__(self):
        return self.user.username

def get_profile(self):
    return UserProfile.objects.get_or_create(user=self)[0]

User.add_to_class("profile", property(get_profile))
