from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser



class user(AbstractUser):
    nickname = models.CharField(max_length=50,blank =True)
    description = models.TextField(max_length=200,blank=True)#set basic decription, blank=true so user don't need add description when register
    class Meta(AbstractUser.Meta):
        pass
