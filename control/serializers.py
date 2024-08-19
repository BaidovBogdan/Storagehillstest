from rest_framework import serializers
from .models import Account, SubscriptionProfile

class SubscriptionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionProfile
        fields = ['free_subscription_expiry', 'paid_subscription_expiry', 'money_count']




class AccountSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='get_value', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'updated', 'created', 'value']
