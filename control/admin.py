from django.contrib import admin
from .models import SubscriptionProfile

@admin.register(SubscriptionProfile)
class SubscriptionProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'free_subscription_expiry', 'paid_subscription_expiry', 'money_count')
    search_fields = ('user__username', 'user__email')
    list_filter = ('free_subscription_expiry', 'paid_subscription_expiry')

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'
