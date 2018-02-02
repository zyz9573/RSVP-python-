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

def answer(request,event_id):
    if request.method == "POST":
        event = get_object_or_404(Event,pk = event_id)
        for question in event.question_set.all():
            question.question_answer = request.POST['question']
            question.save()
        return HttpResponse("Successfull add your answer!")
    else:
        return HttpResponse("Fail to add your answer")

class EventCreate(CreateView):
    model = Event
    fields = ['time','event_title','place','event_infor','event_logo']
    

class EventDelete(DeleteView):
    model =Event
    success_url = reverse_lazy('event:index')

class EventUpdate(UpdateView):
     model = Event
     fields = ['time', 'event_title', 'place', 'event_infor', 'event_logo']

from users.models import realuser
def event_view(request):
    pk = request.GET.get('p1')
    yonghu = realuser.objects.get(id = pk)
    return HttpResponse("this is "+yonghu.username)