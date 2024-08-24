# myapp/management/commands/notify.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from control.models import SubscriptionProfile

class Command(BaseCommand):
    help = 'Notify users with subscriptions expiring in 7 days or less and print email addresses'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        target_date = today + timedelta(days=7)
        
        # Fetch subscriptions expiring in 7 days or less
        subscriptions = SubscriptionProfile.objects.filter(
            free_subscription_expiry__lte=target_date,
            free_subscription_expiry__gte=today
        )

        email_sent = []  # List to keep track of sent emails

        for subscription in subscriptions:
            user = subscription.user
            subject = 'Ваша подписка истекает'
            message = (
                f'Уважаемый пользователь!\n\n'
                f'Мы рады сотрудничать с Вами! '
                'Для продолжения сотрудничества - пожалуйста выберите необходимый Вам период и оплатите его.\n\n'
                'С уважением, команда Storagehills.'
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Use the email address from your settings
                [user.email]
            )
            email_sent.append(user.email)  # Track sent emails

        # Print all email addresses that were notified
        if email_sent:
            self.stdout.write(self.style.SUCCESS('Successfully sent notifications to the following email addresses:'))
            for email in email_sent:
                self.stdout.write(email)
        else:
            self.stdout.write(self.style.SUCCESS('No subscriptions are expiring in the next 7 days.'))
