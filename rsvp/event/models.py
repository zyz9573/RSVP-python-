from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    time = models.CharField(max_length=250)
    event_title = models.CharField(max_length=500)
    place = models.CharField(max_length=100)
    event_infor = models.CharField(max_length=1000)
    event_logo = models.CharField(max_length=1000,blank=True)
    canaddone = models.BooleanField(default = True)
    def get_absolute_url(self):
        return reverse('event:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.event_title + ' - ' + self.time

class questionnaire(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='participants')
    event = models.OneToOneField(Event,on_delete=models.CASCADE)
    def __str__(self):
        return self.event.event_title + "\'s quesionnaire"
    class Meta:
        ordering = ["-created_at"]

class question(models.Model):
    question = models.CharField(max_length=200, verbose_name="question")
    required = models.BooleanField(default=True, help_text="must answer")
    questionnaire = models.ForeignKey(questionnaire,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    order_in_list = models.IntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    vendor = models.ManyToManyField(settings.AUTH_USER_MODEL)
        
    class Meta:
        abstract = True

class choicequestion(question):
    multi_choice = models.BooleanField(default=False,verbose_name="is multiple choice")

class nonchoicequestion(question):
    type = models.SmallIntegerField(verbose_name="non-choice question",
                                    choices=((0,'QA'),(1,'FA')),default=0)

class choice(models.Model):
    question = models.ForeignKey(choicequestion,related_name="choices",on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    multi_choice = models.BooleanField(default=False,verbose_name="is multiple choice")
    order_in_list = models.IntegerField(default=1)

class answersheet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) 
    questionnaire = models.ForeignKey(questionnaire,on_delete=models.CASCADE)     
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

class answer(models.Model):
    answer_sheet = models.ForeignKey(answersheet,on_delete=models.CASCADE)

    class Meta:
        abstract = True

class singlechoiceanswer(answer):
    choice = models.ForeignKey(choice, related_name="single_choice_answers",on_delete=models.CASCADE)  
    question = models.ForeignKey(choicequestion, related_name="single_choice_answer_set",on_delete=models.CASCADE)

class multichoiceanswer(answer):
    choices = models.ManyToManyField(choice, related_name="multi_choice_answers")
    question = models.ForeignKey(choicequestion, related_name="multi_choice_answers",on_delete=models.CASCADE)


class textanswer(answer):
    text = models.TextField()
    question = models.ForeignKey(nonchoicequestion,on_delete=models.CASCADE)


"""
class Question(models.Model):
    Event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_content = models.CharField(max_length=10)
    question_answer = models.CharField(max_length=1000)
    is_favorite = models.BooleanField(default = False)
    def __str__(self):
        return self.question_content

class QuestionMultiple(models.Model):
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_content = models.CharField(max_length=1000)
    Choice = ArrayField(ArrayField( models.CharField(max_length=1000, blank=True)))
    def __str__(self):
        return self.question_content
"""