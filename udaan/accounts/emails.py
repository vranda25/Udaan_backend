from django.core.mail import send_mail
from django.conf import settings
import random
from .models import CustomUser

def send_verification_mail(email,name):
    subject = 'Uddan'
    otp = random.randint(100000, 999999)
    message = f'Hi {name}, Please verify your account. otp : {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    print('mail sent sucessfully')
    user = CustomUser.objects.get(email=email)
    user.otp = otp
    user.save()