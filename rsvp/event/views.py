from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Event,Question
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .form import EventForm
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

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        return super().form.valid(form)

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
    jihe = yonghu.owner_event.all()
    return render(request,'event/myevent.html',context={'jihe':jihe})#HttpResponse("this is "+yonghu.username)

def event_add(request):
    pk = request.GET.get('p1')
    yonghu = realuser.objects.get(id = pk)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            shijian = Event.objects.get(place = request.POST.get('place'))
            yonghu.owner_event.add(shijian);
            return render(request,'users/realuser.html',context={'user_info':yonghu})
    else:
        form = EventForm()
        return render(request,'event/addevent.html',context={'form':form,'user_info':yonghu})