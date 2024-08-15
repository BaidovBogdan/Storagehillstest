# myapp/management/commands/test.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Send a test email to every user'

    def handle(self, *args, **kwargs):
        users = User.objects.all()  # Fetch all users

        for user in users:
            subject = 'Test Email'
            message = 'This is a test email. Please ignore.'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Use the email address from your settings
                [user.email]
            )

        self.stdout.write(self.style.SUCCESS('Successfully sent test emails to all users.'))
