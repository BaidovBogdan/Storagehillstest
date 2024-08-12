from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ip_address', 'created_at')

