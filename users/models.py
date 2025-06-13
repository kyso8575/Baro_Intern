from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.username
