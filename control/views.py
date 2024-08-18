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

    admins = ['bagdanbaidov@yandex.ru']

    message_body = "text"

    message_subject = "subject"

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
        subject=message_subject,
        body=message_body,
        # Replace with your email or settings.DEFAULT_FROM_EMAIL
        to=[recipient_email , admins[0]],
    )
    
    
    # Attach the .docx file
    email.attach('filled_invoice.docx', doc_io.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    # Send the email
    email.send()
    

    return True  # Optionally return True when the function completes successfully





@api_view(['POST'])  # Assuming POST request for sending emails
@permission_classes([IsAuthenticated])  # Require authentication
def payment_email(request):
    
    template_path = os.path.join(settings.MEDIA_ROOT, 'instance.docx')
    send_is = generate_and_send_invoice(request.data,template_path,request.user.email)
    if send_is : 
        return Response({"message": "письмо отправлено!"})
    return Response({"message": "письмо не отправлено"}, status=status.HTTP_400_BAD_REQUEST)

def react_app(request):
    return render(request, 'index.html')

class SubscriptionProfileDetailView(generics.RetrieveAPIView):
    serializer_class = SubscriptionProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        # Получаем профиль подписки текущего аутентифицированного пользователя
        return self.request.user.subscription_profile

