from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response


@receiver(post_save, sender=Response)
def send_response_notification(sender, instance, **kwargs):
    if kwargs['created']:
        send_mail(
            'New Response',
            'You have a new response to your advertisement.',
            'from@example.com',
            [instance.advertisement.user.email],
            fail_silently=False,
        )
