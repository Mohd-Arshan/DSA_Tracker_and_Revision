from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    token_version = models.IntegerField(default=0)  # For token invalidation
    
    USERNAME_FIELD = 'email'    # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = ['username']  # Required when creating a superuser
    
    def __str__(self):
        return self.email
