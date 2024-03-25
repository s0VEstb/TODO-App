from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import OneToOneField


class Profile(models.Model):
    user = OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField()
    bio = models.TextField()
    age = models.IntegerField()

    def __str__(self):
        return self.user.username



class SMScode(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='sms')
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username