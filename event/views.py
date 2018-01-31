from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Event,Question
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

class IndexView(generic.ListView):
    template_name = 'event/index.html'
    context_object_name ='all_events'

    def get_queryset(self):
        return Event.objects.all()

class DetailView(generic.DetailView):
    model = Event
    template_name='event/detail.html'

def answer(reques):

    return

class EventCreate(CreateView):
    model = Event
    fields = ['time','event_title','place','event_infor','event_logo']

class EventDelete(DeleteView):
    model =Event
    success_url = reverse_lazy('event:index')

class EventUpdate(UpdateView):
     model = Event
     fields = ['time', 'event_title', 'place', 'event_infor', 'event_logo']
