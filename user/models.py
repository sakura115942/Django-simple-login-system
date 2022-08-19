import imp
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    is_auth = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username


class EmailVerifyRecord(models.Model):

    email=models.EmailField()
    code = models.CharField(max_length=20)
    send_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
