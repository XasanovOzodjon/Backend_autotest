from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )
    avatar = models.ImageField(upload_to='static/avatars/', default='static/avatars/default.png')
    totalPoints = models.IntegerField(default=0)
    lastActive = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_banned = models.BooleanField(default=False)