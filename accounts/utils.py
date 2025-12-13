import random
from django.core.mail import send_mail
from django.conf import settings

def generate_code():
    return str(random.randint(1000,9999))

def send_verification_email(email,code):
    subjects = "Email Verification code"
    message = f"Your verification code is: {code}"

    send_mail(
        subjects,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False

    )