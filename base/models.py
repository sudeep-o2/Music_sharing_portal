from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    
    name = models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class MusicFile(models.Model):

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    ]

    host=models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)
    allowed_emails = models.TextField(blank=True, null=True)  # Comma-separated list of allowed emails



    def __str__(self):
        return self.title
    