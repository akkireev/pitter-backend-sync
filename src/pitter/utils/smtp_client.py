import ssl
import smtplib

from django.conf import settings


class SmtpClient:
    @classmethod
    def send_mail(cls, email, msg):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.SMTP_HOST_IP, settings.SMTP_HOST_PORT, context=context) as server:
            server.login(settings.SMTP_SENDER_ADDRESS, settings.SMTP_SENDER_PASSWORD)
            server.sendmail(settings.SMTP_SENDER_ADDRESS, email, msg)
