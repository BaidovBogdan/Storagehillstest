from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from control.models import SubscriptionProfile

class Command(BaseCommand):
    help = 'Send email notifications to users with subscriptions expiring in 7 days'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        target_date = today + timedelta(days=7)
        subscriptions = SubscriptionProfile.objects.filter(
            paid_subscription_expiry=target_date
        )

        for subscription in subscriptions:
            user = subscription.user
            subject = 'Your subscription is expiring soon'
            message = (
                f'Hi {user.username},\n\n'
                f'Your subscription is set to expire on {subscription.paid_subscription_expiry}. '
                'Please renew it to avoid any interruption in your services.\n\n'
                'Thank you,\nThe Team'
            )
            send_mail(
                subject,
                message,
                'webmaster@example.com',  # Replace with your email address
                [user.email]
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully sent subscription expiration notifications.'))
