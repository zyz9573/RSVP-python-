from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from event.models import Event 


class realuser(AbstractUser):
    nickname = models.CharField(max_length=50,blank =True)
    description = models.TextField(max_length=200,blank=True)#set basic decription, blank=true so user don't need add description when register
    owner_event = models.ManyToManyField(Event,related_name='owner_event')
    vendor_event = models.ManyToManyField(Event,related_name='vendor_event')
    guest_event = models.ManyToManyField(Event,related_name='guest_event')
    class Meta(AbstractUser.Meta):
        pass