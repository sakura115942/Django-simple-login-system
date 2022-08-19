from django.db.models.signals import post_save
from django.dispatch import receiver

from threading import Thread

from .models import User
from .utils import send_register_email


@receiver(post_save, sender=User)
def post_save_user_request(sender, instance, **kwargs):
    if instance.is_superuser or instance.is_auth:
        return
    else:
        Thread(target=send_register_email, args=(instance.email,)).start()
