from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username