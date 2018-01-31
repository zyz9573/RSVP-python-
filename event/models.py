from django.db import models
from django.urls import reverse
# Create your models here.
class Event(models.Model):
    time = models.CharField(max_length=250)
    event_title = models.CharField(max_length=500)
    place = models.CharField(max_length=100)
    event_infor = models.CharField(max_length=1000)
    event_logo = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('event:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.event_title + ' - ' + self.time

class Question(models.Model):
    Event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_content = models.CharField(max_length=10)
    question_answer = models.CharField(max_length=1000)
    is_favorite = models.BooleanField(default = False)
    def __str__(self):
        return self.question_content
