from django.core.management import call_command
from django.test import TestCase
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from control.models import SubscriptionProfile
from django.conf import settings

class SendExpirationNotificationsTest(TestCase):
    def setUp(self):
        # Set up the test environment
        today = timezone.now().date()
        # Create a test user and subscription profile expiring in 7 days
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        self.subscription = SubscriptionProfile.objects.create(
            user=self.user,
            paid_subscription_expiry=today + timedelta(days=7)  # Set expiry date to 7 days from today
        )
        # Use console backend for testing
        settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    def test_send_expiration_notifications(self):
        # Call the management command
        call_command('send_subscription_notifications')

        # Check that an email has been sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Verify email details
        self.assertEqual(email.subject, 'Your subscription is expiring soon')
        self.assertEqual(email.to, ['testuser@example.com'])
        self.assertIn('Your subscription is set to expire on', email.body)
