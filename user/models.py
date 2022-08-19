import imp
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    is_auth = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
