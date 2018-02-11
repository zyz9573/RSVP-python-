from django import forms
from django.contrib.auth.models import User

from .models import Event,questionnaire,choicequestion,nonchoicequestion,choice,answersheet,singlechoiceanswer,multichoiceanswer,textanswer#, Question


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['time', 'event_title', 'place', 'event_infor', 'canaddone']


class choicequestionform(forms.ModelForm):
	class Meta:
		model = choicequestion
		fields = ['question']

class nonchoicequestionform(forms.ModelForm):
	class Meta:
		model = nonchoicequestion
		fields = ['question']