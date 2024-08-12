from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import SubscriptionProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_subscription_profile(sender, instance, created, **kwargs):
    if created:
        SubscriptionProfile.objects.create(user=instance)
