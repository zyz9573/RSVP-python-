from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

#from users.models import realuser
# Create your models here.
class Event(models.Model):
    time = models.CharField(max_length=250)
    event_title = models.CharField(max_length=500)
    place = models.CharField(max_length=100)
    event_infor = models.CharField(max_length=1000)
    event_logo = models.CharField(max_length=1000,blank=True)
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    #event_owner = models.ManyToManyField(realuser,related_name='event_owner')
    #event_vendor = models.ManyToManyField(realuser,related_name='event_vendor')
    #event_guest = models.ManyToManyField(realuser,related_name='event_guest')
    def get_absolute_url(self):
        return reverse('event:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.event_title + ' - ' + self.time

class Question(models.Model):
    Event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_content = models.CharField(max_length=1000)
    question_answer = models.CharField(max_length=1000)
    is_favorite = models.BooleanField(default = False)
    def __str__(self):
        return self.question_content

class QuestionMultiple(models.Model):
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_content = models.CharField(max_length=1000)
    #Choice = ArrayField(ArrayField( models.CharField(max_length=1000, blank=True)))
    #Choice  = text[][]
    def __str__(self):
        return self.question_content

class Options(models.Model):
    Multiple = models.ForeignKey(QuestionMultiple, on_delete=models.CASCADE)
    option_content = models.CharField(max_length=1000)

    def __str__(self):
        return self.option_content
