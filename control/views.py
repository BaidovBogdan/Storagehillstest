from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
import yadisk
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .models import SubscriptionProfile
from .serializers import SubscriptionProfileSerializer

from config.settings import YANDEX_DISK_TOKEN
y = yadisk.YaDisk(token=YANDEX_DISK_TOKEN)



@api_view(['POST'])  # Assuming POST request for sending emails
@permission_classes([IsAuthenticated])  # Require authentication
def payment_email(request):
    # Extract tariff and INN from the request data
    tariff = request.data.get('tariff')
    inn = request.data.get('inn')

    if not tariff or not inn:
        return Response({"error": "Tariff and INN are required."}, status=400)

    # Get list of admin emails
    admins = ['bagdanbaidov@yandex.ru']  # List format

    # Assuming the user is logged in and has an email
    customer_emails = [request.user.email]  # List format

    # Construct the email message
    message = f"""
    Уважаемый {inn},

    Спасибо что пользуетесь нашим сервисом.

    Выбранный тариф: {tariff}
    Оплатите подписку в ближайшее время. 
    Реквизиты находятся на сайте.
    И в скором времени ваша подписка будет активирована.


    StorageHills
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





y = yadisk.YaDisk(token=YANDEX_DISK_TOKEN)

from django.http import StreamingHttpResponse

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def management(request):
    path = f'/{request.user.username}/'

    if request.method == 'GET':
        try:
            files = y.listdir(path)
            file_responses = {}

            for file in files:
                print(files)
                file_path = file['path']
                file_content = y.download(path,file['name'])
                file_responses[file['name']] = StreamingHttpResponse(file_content, content_type='application/octet-stream')

            return Response(file_responses, status=status.HTTP_200_OK)
        except yadisk.exceptions.PathNotFoundError:
            return Response({'detail': 'Directory not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':
        uploaded_files = request.FILES  # Получаем загруженные файлы из запроса

        if not uploaded_files:
            return Response({'status': 'error', 'message': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        for file in uploaded_files.values():
            try:
                y.upload(file, f'{path}/{file.name}')
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'status': 'success', 'message': 'Files uploaded'}, status=status.HTTP_200_OK)