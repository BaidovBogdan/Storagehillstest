from django.contrib import admin
from .models import SubscriptionProfile , Account

@admin.register(SubscriptionProfile)
class SubscriptionProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'free_subscription_expiry', 'paid_subscription_expiry', 'money_count')
    search_fields = ('user__username', 'user__email')
    list_filter = ('free_subscription_expiry', 'paid_subscription_expiry')

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'



@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('profile_user_username', 'updated', 'created')
    search_fields = ('profile__user__username', 'profile__user__email')
    list_filter = ('created', 'updated')

    def profile_user_username(self, obj):
        return obj.profile.user.username
    profile_user_username.short_description = 'Username'