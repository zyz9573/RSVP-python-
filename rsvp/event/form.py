from django import forms
from django.contrib.auth.models import User

from .models import Event, Question


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['time', 'event_title', 'place', 'event_infor', 'event_logo']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']