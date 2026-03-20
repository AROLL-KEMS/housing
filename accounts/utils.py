import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user, otp):

    subject = "Verify your Housing Locator Account"

    message = f"""
Hello {user.username},

Your verification code is:

{otp}

Enter this code to verify your account.

Thank you.
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )