from datetime import timedelta
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .serializers import UserRegistrationSerializer
from .models import RegistrationAttempt
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def get_queryset(self):
        return User.objects.none()

    def post(self, request, *args, **kwargs):
        ip_address = self.get_client_ip(request)
        if self.is_ip_blocked(ip_address):
            raise ValidationError("Вы можете больше чем 1 аккаунт!.")

        response = super().post(request, *args, **kwargs)
        user = self.get_serializer().instance
        RegistrationAttempt.objects.create(ip_address=ip_address, user=user)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_ip_blocked(self, ip_address):
        recent_attempts = RegistrationAttempt.objects.filter(
            ip_address=ip_address,
            created_at__gte=now() - timedelta(minutes=15)
        ).count()
        return recent_attempts >= 1