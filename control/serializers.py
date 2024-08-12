from rest_framework import serializers
from .models import SubscriptionProfile

class SubscriptionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionProfile
        fields = ['free_subscription_expiry', 'paid_subscription_expiry', 'money_count']
