from django.urls import path
from .views import SubscriptionProfileDetailView, management

urlpatterns = [
    path('subscription-profile/', SubscriptionProfileDetailView.as_view(), name='subscription-profile-detail'),
    path('management/', management, name='management'),
]