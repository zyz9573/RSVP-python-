from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Event,Question,QuestionMultiple
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
    as_owner = yonghu.owner_event.all()
    as_vendor = yonghu.vendor_event.all()
    as_guest = yonghu.guest_event.all()
    return render(request,'event/myevent.html',context={'as_owner':as_owner,'as_vendor':as_vendor,'as_guest':as_guest,'user':pk})#HttpResponse("this is "+yonghu.username)

def event_add(request):
    pk = request.GET.get('p1')
    yonghu = realuser.objects.get(id = pk)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            shijian = Event.objects.get(time = request.POST.get('time'))
            yonghu.owner_event.add(shijian)
            return render(request,'users/realuser.html',context={'user_info':yonghu})
    else:
        form = EventForm()
        return render(request,'event/addevent.html',context={'form':form,'user_info':yonghu})

def event_detail(request):
    pk = request.GET.get('p2')
    shijian = Event.objects.get(id = pk)
    pku = request.GET.get('p1')
    yonghu = realuser.objects.get(id =pku)
    return render(request,'event/eventdetail.html',context={'event_info':shijian,'user':yonghu})

def inviteowner(request):
    pk = request.GET.get('p1')
    if request.method=='POST':
        shijian = Event.objects.get(id = pk)
        yonghu = realuser.objects.get(username = request.POST['invite_username'])
        yonghu.owner_event.add(shijian)
        return render(request,'event/eventdetail.html',context={'event_info':shijian})
    else:
        return render(request,'event/inviteowner.html',context={'id':pk})

def invitevendor(request):
    pk = request.GET.get('p1')
    if request.method=='POST':
        shijian = Event.objects.get(id = pk)
        yonghu = realuser.objects.get(username = request.POST['invite_username'])
        yonghu.vendor_event.add(shijian)
        return render(request,'event/eventdetail.html',context={'event_info':shijian})
    else:
        return render(request,'event/invitevendor.html',context={'id':pk})

def inviteguest(request):
    pk = request.GET.get('p1')
    if request.method=='POST':
        shijian = Event.objects.get(id = pk)
        yonghu = realuser.objects.get(username = request.POST['invite_username'])
        yonghu.guest_event.add(shijian)
        return render(request,'event/eventdetail.html',context={'event_info':shijian})
    else:
        return render(request,'event/inviteguest.html',context={'id':pk})

def editQuestion(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id=pk)
    return render(request, 'event/editQuestion.html', context={'event_info': shijian})




def addMultiple(request):
    pk = request.GET.get('p1')
    event = Event.objects.get(id = pk)
    A = QuestionMultiple()
    A.question_content = ''
    A.Event = event
    A.Choice = []
    A.save()
    return render(request, 'event/addMultiple.html', context={'event_info':event,'question' : A})

def addText(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id=pk)
    pku = request.GET.get('p1')
    yonghu = realuser.objects.get(id=pku)
    A = Question()
    A.question_content = ''
    A.question_answer = ''
    A.Event = shijian
    A.save()
    return render(request, 'event/addText.html', context={'event_info': shijian, 'question': A })

def addQuestion(request):
    pk2 = request.GET.get('p2')
    if request.method == "POST":
        A = Question.objects.get(id = pk2)
        A.question_content = request.POST['question']
        A.save()
        return HttpResponse("Successfull add your question!")
    else:
        return HttpResponse("Fail to add your question")

def addOption(request):                #used for going to add options page
    pk1 = request.GET.get('p1')
    pk2 = request.GET.get('p2')
    pk3 = request.GET.get('p3')
    shijian = Event.objects.get(id = pk1)
    A = QuestionMultiple.objects.get(id = pk2)
    if pk3 == A.Choice.size():
        option = ''
    else:
        option = pk3

    return render(request, 'event/addOption.html', context={'event_info': shijian, 'question' : A,'option': option})

def addOptionA(request):             #used for add options' submit
    pk1 = request.GET.get('p1')
    pk2 = request.GET.get('p2')
    pk3 = request.GET.get('p3')
    if request.method == "POST":
        event = Event.objects.get(id = pk1)
        A = QuestionMultiple.objects.get(id = pk2)
        if pk3 == A.Choice.size():
            A.Choice.append(request.POST['option'])
        else:
            A.Choice[pk3]=(request.POST['option'])
        A.save()
        return render(request, 'event/addMultiple.html', context={'event_info': event, 'question' : A})
    else:
        return HttpResponse("Fail to add your question")

def addMultipleChoice(request):
    pk1 = request.GET.get('p1')
    pk2 = request.GET.get('p2')
    if request.method == "POST":
        event = Event.objects.get(id=pk1)
        A = QuestionMultiple.objects.get(id = pk2)
        A.question_content = request.POST['question']
        A.Event = event
        A.save()
        return HttpResponse("Successfull add your question!")
    else:
        return HttpResponse("Fail to add your question")

def deleteQuestion(request):
    pk1 = request.GET.get('p1')
    pk2 = request.GET.get('p2')
    if request.method == "POST":
        event = Event.objects.get(id=pk1)
        A = Question.objects.get(id=pk2)
        A.delete()
        return HttpResponse("Successfully delete your question")
    else:
        return HttpResponse("Fail to delete your question")

def deleteMultipleQuestion(request):
    pk1 = request.GET.get('p1')
    pk2 = request.GET.get('p2')
    if request.method == "POST":
        event = Event.objects.get(id=pk1)
        A = QuestionMultiple.objects.get(id=pk2)
        A.delete()
        return HttpResponse("Successfully delete your question")
    else:
        return HttpResponse("Fail to delete your question")

def updateQuestion(request):
    pk1 = request.GET.get('p1')
    event = Event.objects.get(id=pk1)
    pk2 = request.GET.get('p2')
    question = Question.objects.get(id=pk2)
    return render(request, 'event/addText.html', context={'event': event, 'question':question})

def updateMultipleQuestion(request):
    pk1 = request.GET.get('p1')
    event = Event.objects.get(id=pk1)
    pk2 = request.GET.get('p2')
    question = QuestionMultiple.objects.get(id=pk2)
    return render(request, 'event/addMultiple.html', context={'event': event, 'question': question})
