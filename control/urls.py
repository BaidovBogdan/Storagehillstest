from django.urls import path
from .views import SubscriptionProfileDetailView, payment_email

urlpatterns = [
    path('subscription-profile/', SubscriptionProfileDetailView.as_view(), name='subscription-profile-detail'),
    path('send-payment-email/', payment_email, name='send_payment_email'),
]