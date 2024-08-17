from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .models import SubscriptionProfile
from .serializers import SubscriptionProfileSerializer

from config.settings import YANDEX_DISK_TOKEN



@api_view(['POST'])  # Assuming POST request for sending emails
@permission_classes([IsAuthenticated])  # Require authentication
def payment_email(request):
    print(request.data)
    # Extract tariff and INN from the request data
    tariff = request.data.get('tariff')
    inn = request.data.get('inn')
    period = request.data.get('period')

    if not tariff or not inn or not period:
        return Response({"error": "Tariff, INN, and period are required."}, status=400)

    # Get list of admin emails
    admins = ['bagdanbaidov@yandex.ru']  # List format

    # Assuming the user is logged in and has an email
    customer_emails = [request.user.email]  # List format

    # Construct the email message
    message = f"""
    Уважаемый {inn},

    Спасибо, что пользуетесь нашим сервисом.

    Выбранный тариф: {tariff}
    Период подписки: {period}

    Пожалуйста, оплатите подписку в ближайшее время. 
    Реквизиты находятся на сайте, и вскоре ваша подписка будет активирована.

    С уважением,
    Команда StorageHills
    """
    subject = 'Оплата StorageHills'

    # Send email to admins
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        admins,
        fail_silently=False,
    )

    # Send email to customers
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        customer_emails,
        fail_silently=False,
    )

    return Response({"message": "Emails sent successfully!"})

def react_app(request):
    return render(request, 'index.html')

class SubscriptionProfileDetailView(generics.RetrieveAPIView):
    serializer_class = SubscriptionProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        # Получаем профиль подписки текущего аутентифицированного пользователя
        return self.request.user.subscription_profile

