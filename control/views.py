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



from docx import Document
from io import BytesIO
from django.core.mail import EmailMessage
import os

def generate_and_send_invoice(context, template_path, recipient_email):
    """
    Generate a .docx invoice, replace placeholders, and send it via email.

    :param context: A dictionary containing the data to replace placeholders in the template.
    :param template_path: The path to the .docx template file.
    :param recipient_email: The email address to send the invoice to.
    """
    # Load the template document
    doc = Document(template_path)

    # Replace placeholders with actual data in paragraphs
    for paragraph in doc.paragraphs:
        for key, value in context.items():
            if f'{{{key}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{key}}}', str(value))

    # Replace placeholders with actual data in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in context.items():
                    if f'{{{key}}}' in cell.text:
                        cell.text = cell.text.replace(f'{{{key}}}', str(value),)
    # Save the modified document to a BytesIO object (in-memory file)
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)  # Move the cursor to the beginning of the file

    # Prepare the email
    email = EmailMessage(
        subject='Generated Invoice',
        body='Please find the attached invoice document.',
        # Replace with your email or settings.DEFAULT_FROM_EMAIL
        to=[recipient_email],
    )
    
    # Attach the .docx file
    email.attach('filled_invoice.docx', doc_io.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    # Send the email
    email.send()

    return True  # Optionally return True when the function completes successfully





@api_view(['POST'])  # Assuming POST request for sending emails
@permission_classes([IsAuthenticated])  # Require authentication
def payment_email(request):
    context = {
  "tariff": "24000 руб.",
  "inn": "1234567899",
  "period": "12 месяцев",
  "price": "24000 руб.",
  "account_number": "1-18.08.24",
  "date": "18.08.2024",
  "time": "12 месяцев",
  "semi_price": "2000 руб./мес",
  "quantity": "1",
  "priceStr": "двадцать четыре тысячи",
  "quantityStr": "один",
  "recipient": "Криворучко Евгений Витальевич",
  "payer": "Захарченко Михаил Юрьевич"
}
    template_path = os.path.join(settings.MEDIA_ROOT, 'instance.docx')
    generate_and_send_invoice(request.data,template_path,request.user.email)

    
    garbage="""
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
    message = f
    Уважаемый {inn},

    Спасибо, что пользуетесь нашим сервисом.

    Выбранный тариф: {tariff}
    Период подписки: {period}

    Пожалуйста, оплатите подписку в ближайшее время. 
    Реквизиты находятся на сайте, и вскоре ваша подписка будет активирована.

    С уважением,
    Команда StorageHills
    
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
"""
    return Response({"message": "Emails sent successfully!"})

def react_app(request):
    return render(request, 'index.html')

class SubscriptionProfileDetailView(generics.RetrieveAPIView):
    serializer_class = SubscriptionProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        # Получаем профиль подписки текущего аутентифицированного пользователя
        return self.request.user.subscription_profile

