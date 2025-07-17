from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserPlan

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_plan(sender, instance, created, **kwargs):
    if created:
        UserPlan.objects.create(user=instance)