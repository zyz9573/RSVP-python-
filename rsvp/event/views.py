from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Event,questionnaire,choicequestion,nonchoicequestion,choice,answersheet,singlechoiceanswer,multichoiceanswer,textanswer#,Question,QuestionMultiple
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .form import EventForm, choicequestionform,nonchoicequestionform
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
    yonghu = realuser.objects.get(id = request.user.id)
    as_owner = yonghu.owner_event.all()
    as_vendor = yonghu.vendor_event.all()
    as_guest = yonghu.guest_event.all()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            shijian = Event.objects.get(time = request.POST.get('time'))
            yonghu.owner_event.add(shijian)
            questionnaire.objects.create(event = shijian)
            return render(request,'users/realuser1.html',context={'user_info':yonghu,'owner':as_owner,'vendor':as_vendor,'guest':as_guest})
    else:
        form = EventForm()
        return render(request,'event/addevent.html',context={'form':form,'user_info':yonghu})

def event_detail(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id = pk)
    pku = request.user.id
    yonghu = realuser.objects.get(id =pku)
    return render(request,'event/eventdetail.html',context={'event_info':shijian,'user':yonghu})

def event_detail_owner(request):
    pk = request.GET.get('p1')
    yonghu = realuser.objects.get(id = request.user.id)
    shijian = Event.objects.get(id = pk)
    xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    if request.GET.get('p2') == 'delete':
        Event.objects.get(id=pk).delete()
        as_owner = yonghu.owner_event.all()
        as_vendor = yonghu.vendor_event.all()
        as_guest = yonghu.guest_event.all()
        return render(request,'users/realuser1.html',context={'user_info':yonghu,'owner':as_owner,'vendor':as_vendor,'guest':as_guest})
    if yonghu.owner_event.filter(id = pk).exists():
        return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})
    else:
        return render(request,'users/realuser1.html')

def event_detail_vendor(request):
    pk = request.GET.get('p1')
    yonghu = realuser.objects.get(id = request.user.id)#current login user
    shijian = Event.objects.get(id = pk)#current event
    if yonghu.vendor_event.filter(id = pk).exists():
        xuanze = choicequestion.objects.filter(vendor = yonghu)
        wenda = nonchoicequestion.objects.filter(vendor = yonghu)
        info = ["action","state","question"]
        schoicelist = [info]
        info = ["multi choice question"]
        mchoicelist = [info]
        info = ["text question"]
        textlist = [info]
        for q in yonghu.choicequestion_set.filter(questionnaire = shijian.questionnaire).all():
            temp = "temp"
            if not q.is_active:
                temp = "finalized"
            else:
                temp = "active   "            
            if q.multi_choice:
                mchoicelist.append([temp,q.question])
            else:
                schoicelist.append([temp,q.question])
        for q in yonghu.nonchoicequestion_set.filter(questionnaire = shijian.questionnaire).all():
            if not q.is_active:
                temp = "finalized"
            else:
                temp = "active   " 
            textlist.append([temp,q.question])
        for user in shijian.guest_event.all():
            schoicelist[0].append(user.username)
            i=1
            j=1
            for q in yonghu.choicequestion_set.filter(questionnaire = shijian.questionnaire).all():
                if q.multi_choice:
                    if user.answersheet_set.filter(questionnaire=shijian.questionnaire).exists():
                        answersheet = user.answersheet_set.get(questionnaire=shijian.questionnaire)
                        answers = answersheet.multichoiceanswer_set.filter(question = q).all()
                        ans=''
                        for answer in answers:
                            ans=ans+answer.choices.get().description+';'
                        mchoicelist[j].append(ans)
                    else:
                        mchoicelist[j].append("NOT ANSWER YET")
                    ++j
                else:
                    if user.answersheet_set.filter(questionnaire=shijian.questionnaire).exists():
                        answersheet = user.answersheet_set.get(questionnaire=shijian.questionnaire)
                        if answersheet.singlechoiceanswer_set.filter(question = q).exists():
                            answer = answersheet.singlechoiceanswer_set.get(question = q).choice.description    
                            schoicelist[i].append(answer)
                    else:
                        schoicelist[i].append("NOT ANSWER YET")      
                    ++i                    
            i=1
            for q in yonghu.nonchoicequestion_set.filter(questionnaire = shijian.questionnaire).all():
                if user.answersheet_set.filter(questionnaire=shijian.questionnaire).exists():
                    answersheet = user.answersheet_set.get(questionnaire=shijian.questionnaire)
                    if answersheet.textanswer_set.filter(question = q).exists():
                        answer = answersheet.textanswer_set.get(question = q).text
                        textlist[i].append(answer)
                else:
                    textlist[i].append("NOT ANSWER YET")
                ++i
        return render(request,'event/event_detail_vendor.html',context={'ini':schoicelist[0],'sl':schoicelist[1:],'ml':mchoicelist[1:],'tl':textlist[1:],'event_info':shijian,'choiceq':xuanze,'textq':wenda})
    else:
        return render(request,'users/realuser1.html')

def event_detail_guest(request):
    pk = request.GET.get('p1')
    yonghu = realuser.objects.get(id = request.user.id)
    shijian = Event.objects.get(id = pk)
    xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    if yonghu.guest_event.filter(id = pk).exists():
        if yonghu.answersheet_set.filter(questionnaire = shijian.questionnaire).exists():
            daanbiao = yonghu.answersheet_set.get(questionnaire = shijian.questionnaire)
            if request.method == "POST":
                for q in xuanze:
                    if q.is_active:
                        if q.multi_choice:
                            if q.multi_choice_answers.exists():
                                q.multi_choice_answers.filter(answer_sheet = daanbiao).all().delete()
                                xid_list = request.POST.getlist(str(q.id))
                                for xid in xid_list:
                                    duoxuandaan = multichoiceanswer.objects.create(answer_sheet = daanbiao,question=q)
                                    xuanxiang = q.choices.get(id = int(xid))
                                    xuanxiang.multi_choice_answers.add(duoxuandaan)                            
                            else:
                                xid_list = request.POST.getlist(str(q.id))
                                for xid in xid_list:
                                    duoxuandaan = multichoiceanswer.objects.create(answer_sheet = daanbiao,question=q)
                                    xuanxiang = q.choices.get(id = int(xid))
                                    xuanxiang.multi_choice_answers.add(duoxuandaan)
                        else:
                            if q.single_choice_answer_set.filter(answer_sheet = daanbiao).exists():
                                xid = request.POST.get(str(q.id))
                                xuanxiang = q.choices.get(id =int(xid))
                                singlechoiceanswer.objects.get(answer_sheet = daanbiao,question = q).delete()
                                singlechoiceanswer.objects.create(answer_sheet = daanbiao,question = q,choice = xuanxiang)
                            else:
                                xid = request.POST.get(str(q.id))
                                xuanxiang = q.choices.get(id = int(xid))
                                singlechoiceanswer.objects.create(answer_sheet = daanbiao,question = q,choice = xuanxiang)
                for q in wenda:
                    if q.is_active:
                        if q.textanswer_set.filter(answer_sheet = daanbiao).exists():
                            q.textanswer_set.get(answer_sheet = daanbiao,question = q).delete()
                            textanswer.objects.create(answer_sheet = daanbiao,question = q, text = request.POST.get(str(q.id)))
                        else:
                            textanswer.objects.create(answer_sheet = daanbiao,question = q, text = request.POST.get(str(q.id)))
            return render(request,'event/event_detail_guest.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda,'daanbiao':daanbiao})
        else:
            #corrospond answer sheet doesn' texist yet
            answersheet.objects.create(user = yonghu,questionnaire = shijian.questionnaire)
            shijian.questionnaire.participants.add(yonghu)
            return render(request,'event/event_detail_guest.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda}) 
    else:
        return render(request,'users/realuser1.html')

def inviteowner(request):
    pk = request.GET.get('p1')
    if request.method=='POST':
        shijian = Event.objects.get(id = pk)
        xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        if realuser.objects.filter(username = request.POST['invite_username']):
            yonghu = realuser.objects.get(username = request.POST['invite_username'])
            yonghu.owner_event.add(shijian)
        else:
            return HttpResponse("NO SUCH USER")
        return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})
    else:
        return render(request,'event/inviteowner.html',context={'id':pk})

def invitevendor(request):
    pk = request.GET.get('p1')
    if request.method=='POST':
        shijian = Event.objects.get(id = pk)
        xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        if realuser.objects.filter(username = request.POST['invite_username']):
            yonghu = realuser.objects.get(username = request.POST['invite_username'])
            yonghu.vendor_event.add(shijian)
        else:
            return HttpResponse("NO SUCH USER")
        return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})
    else:
        return render(request,'event/invitevendor.html',context={'id':pk})

def inviteguest(request):
    pk = request.GET.get('p1')
    if request.method=='POST':
        shijian = Event.objects.get(id = pk)
        xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        if realuser.objects.filter(username = request.POST['invite_username']):
            yonghu = realuser.objects.get(username = request.POST['invite_username'])
            yonghu.guest_event.add(shijian)
        else:
            return HttpResponse("NO SUCH USER")
        return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})
    else:
        return render(request,'event/inviteguest.html',context={'id':pk})

def editQuestion(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id=pk)
    return render(request, 'event/editQuestion.html', context={'event_info': shijian})


def addmultichoicequestion(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id = pk)
    wenjuan = shijian.questionnaire
    xuanze = choicequestion.objects.filter(questionnaire = wenjuan)
    wenda = nonchoicequestion.objects.filter(questionnaire = wenjuan)
    flag = 'choice'
    cid=request.GET.get('p2')
    if cid:
        choicequestion.objects.get(id = cid).delete()
        form = choicequestionform();
        return render(request,'event/amcq.html',context={'questionnaire': wenjuan,'choiceq':xuanze,'nonchoiceq':wenda,'event':shijian,'form':form,'flag':flag})
    if request.method =='POST':
        temp = choicequestion.objects.create(questionnaire = wenjuan)
        temp.question=request.POST.get('question')
        temp.save()
        form = choicequestionform();
        if shijian.guest_event.exists():
            subject = 'Email notification from RSVP'
            message = shijian.event_title +'has added new question, please check'
            recipient = []
            for user in shijian.guest_event.all():
                recipient.append(user.email)
            send_mail(subject,message,'panjoyzhang95@gmail.com',recipient)
        return render(request,'event/amcq.html',context={'questionnaire': wenjuan,'choiceq':xuanze,'nonchoiceq':wenda,'event':shijian,'form':form,'flag':flag})
    else:
        form = choicequestionform();
        return render(request,'event/amcq.html',context={'questionnaire': wenjuan,'choiceq':xuanze,'nonchoiceq':wenda,'event':shijian,'form':form,'flag':flag})

def addtextquestion(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id = pk)
    wenjuan = shijian.questionnaire
    xuanze = choicequestion.objects.filter(questionnaire = wenjuan)
    wenda = nonchoicequestion.objects.filter(questionnaire = wenjuan)
    flag = 'text'
    tid=request.GET.get('p2')
    if tid:
        nonchoicequestion.objects.get(id = tid).delete()
        form = nonchoicequestionform();
        return render(request,'event/amcq.html',context={'questionnaire': wenjuan,'choiceq':xuanze,'nonchoiceq':wenda,'event':shijian,'form':form,'flag':flag})
    if request.method =='POST':
        temp = nonchoicequestion.objects.create(questionnaire = wenjuan)
        temp.question=request.POST.get('question')
        temp.save()
        form = nonchoicequestionform();
        if shijian.guest_event.exists():
            subject = 'Email notification from RSVP'
            message = shijian.event_title +'has added new question, please check'
            recipient = []
            for user in shijian.guest_event.all():
                recipient.append(user.email)
            send_mail(subject,message,'panjoyzhang95@gmail.com',recipient)
        return render(request,'event/amcq.html',context={'questionnaire': wenjuan,'choiceq':xuanze,'nonchoiceq':wenda,'event':shijian,'form':form,'flag':flag})
    else:
        form = nonchoicequestionform();
        return render(request,'event/amcq.html',context={'questionnaire': wenjuan,'choiceq':xuanze,'nonchoiceq':wenda,'event':shijian,'form':form,'flag':flag})

def editevent(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id = pk)
    xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    flag = request.GET.get('p2')
    if request.method == 'POST':
        if flag == 'title':
            shijian.event_title = request.POST.get('cd')
        elif flag == 'time':
            shijian.time = request.POST.get('cd')
        elif flag == 'place':
            shijian.place = request.POST.get('cd')
        elif flag == 'info':
            shijian.event_infor = request.POST.get('cd')
        shijian.save()
        subject = 'Email notification from RSVP'
        message = shijian.event_title +'has changed, please check'
        from_mail = 'panjoyzhang95@gmail.com'
        recipient = []
        for user in shijian.guest_event.all():
            recipient.append(user.email)
        send_mail(subject,message,from_mail,recipient)
        return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})        
    else:
        return render(request, 'event/modifyevent.html',context={'flag':flag,'event':shijian})



def editmultichoicequestion(request):
    pk = request.GET.get('p2')
    action = request.GET.get('p3')
    duoxuan = choicequestion.objects.get(id = pk)
    if action=='no':
        return render(request,'event/emcq.html',context={'question':duoxuan,'action':action})
    elif action=='add':
        if request.GET.get('p5')=='submit':
            new = choice.objects.create(question = duoxuan,description = request.POST.get("cd"),multi_choice=True)
            new.save()
            action='no'
        elif request.GET.get('p5')=='flip':
            duoxuan.multi_choice=True
            duoxuan.save()
            action='no'
            return render(request,'event/emsq.html',context={'question':duoxuan,'action':action,})
        return render(request,'event/emcq.html',context={'question':duoxuan,'action':action})
    else:
        cid = action
        action=request.GET.get('p4')
        if action=='delete':
            choice.objects.get(id=cid).delete()
            action='no'
            return render(request,'event/emcq.html',context={'question':duoxuan,'action':action})
        elif action=='modify':
            xuanxiang = choice.objects.get(id=cid)
            action='no'
            return render(request,'event/modify.html',context={'question':duoxuan,'action':action,'choice':xuanxiang})

def editsinglechoicequestion(request):
    pk = request.GET.get('p2')
    action = request.GET.get('p3')
    duoxuan = choicequestion.objects.get(id = pk)
    if action=='no':
        return render(request,'event/emsq.html',context={'question':duoxuan,'action':action})
    elif action=='add':
        if request.GET.get('p5')=='submit':
            new = choice.objects.create(question = duoxuan,description = request.POST.get("cd"))
            new.save()
            action='no'
        elif request.GET.get('p5')=='flip':
            duoxuan.multi_choice=True
            duoxuan.save()
            action='no'
            return render(request,'event/emcq.html',context={'question':duoxuan,'action':action})
        return render(request,'event/emsq.html',context={'question':duoxuan,'action':action})
    else:
        cid = action
        action=request.GET.get('p4')
        if action=='delete':
            choice.objects.get(id=cid).delete()
            action='no'
            return render(request,'event/emsq.html',context={'question':duoxuan,'action':action})
        elif action=='modify':
            xuanxiang = choice.objects.get(id=cid)
            action='no'
            return render(request,'event/modify.html',context={'question':duoxuan,'action':action,'choice':xuanxiang})


def modifychoice(request):
    pk = request.GET.get('p1')
    xuanxiang = choice.objects.get(id =pk)
    xuanxiang.description = request.POST.get("cd")
    xuanxiang.save()
    shijian = choice.question.questionnaire.event.all()[0]
    subject = 'Email notification from RSVP'
    message = shijian.event_title +'has changed, please check'
    recipient = []
    for user in shijian.guest_event.all():
        recipient.append(user.email)
    send_mail(subject,message,'panjoyzhang95@gmail.com',recipient)
    duoxuan=xuanxiang.question
    action='no'
    return render(request,'event/emcq.html',context={'question':duoxuan,'action':action})

def modifytext(request):
    pk = request.GET.get('p1')
    shijian = Event.objects.get(id = pk)
    wenjuan = shijian.questionnaire
    xuanze = choicequestion.objects.filter(questionnaire = wenjuan)
    wenda = nonchoicequestion.objects.filter(questionnaire = wenjuan)
    flag = 'text'
    form = nonchoicequestionform()
    pk = request.GET.get('p2')
    textquestion = nonchoicequestion.objects.get(id =pk)
    if request.method == 'POST':
        textquestion.question = request.POST.get("cd")
        textquestion.save()
        subject = 'Email notification from RSVP'
        message = shijian.event_title +'has changed, please check'
        recipient = []
        for user in shijian.guest_event.all():
            recipient.append(user.email)
        send_mail(subject,message,'panjoyzhang95@gmail.com',recipient)
        return render(request,'event/amcq.html',context={'questionnaire': wenjuan,'choiceq':xuanze,'nonchoiceq':wenda,'event':shijian,'form':form,'flag':flag})
    else:
        return render(request,'event/modifytext.html',context={'event':shijian,'textq':textquestion})

def modifychoicequestion(request):
    choiceq = choicequestion.objects.get(id = request.GET.get('p2'))
    action = 'no'
    if request.method == 'POST':
        choiceq.question = request.POST.get("cd")
        choiceq.save()
        shijian = choiceq.questionnaire.event.all()[0]
        subject = 'Email notification from RSVP'
        message = shijian.event_title +'has changed, please check'
        recipient = []
        for user in shijian.guest_event.all():
            recipient.append(user.email)
        send_mail(subject,message,'panjoyzhang95@gmail.com',recipient)
        if choicequestion.multi_choice:
            return render(request,'event/emcq.html',context={'question':choiceq,'action':action})
        else:
            return render(request,'event/emsq.html',context={'question':choiceq,'action':action})
    else:
        return render(request,'event/modifychoicequestion.html',context={'choiceq':choiceq})

def allvendor(request):
    shijian = Event.objects.get(id = request.GET.get('p1'))
    allvendor = shijian.vendor_event.all()
    if allvendor.exists():
        return render(request,'event/allvendor.html',context={'event':shijian,'allvendor':allvendor})
    else:
        xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
        return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})

def setvendorauthority(request):
    shijian = Event.objects.get(id = request.GET.get('p1'))
    vendor = shijian.vendor_event.filter(id = request.GET.get('p2'))
    xuanze = choicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    wenda = nonchoicequestion.objects.filter(questionnaire = shijian.questionnaire).all()
    if vendor.exists():
        vendor = vendor.get(id = request.GET.get('p2'))
        if request.method == 'POST':
            questionlist = request.POST.getlist('choicequestion')
            for question in questionlist:
                question = xuanze.get(id = int(question))
                question.vendor.add(vendor)
            questionlist = request.POST.getlist('nonchoicequestion')
            for question in questionlist:
                question = wenda.get(id = int(question))
                question.vendor.add(vendor)
            return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})
        else:
            return render(request,'event/setvendorauthority.html',context={'event':shijian,'vendor':vendor})
    else:
        return render(request,'event/event_detail_owner.html',context={'event_info':shijian,'choiceq':xuanze,'textq':wenda})

def finalization(request):
    pk = request.GET.get('p1')
    li = request.GET.get('p2')
    qn = li.split(',')[1]
    #
    qn = str(qn[2:len(qn)-1])
    
    yonghu = realuser.objects.get(id = request.user.id)
    shijian = Event.objects.get(id = pk)
    if yonghu.vendor_event.filter(id = pk).exists():
        xuanze = choicequestion.objects.filter(vendor = yonghu)
        wenda = nonchoicequestion.objects.filter(vendor = yonghu)
        if choicequestion.objects.filter(question = qn,vendor = yonghu).exists():
            temp = choicequestion.objects.get(question = qn,vendor = yonghu)
            temp.is_active = not temp.is_active
            temp.save()
        elif nonchoicequestion.objects.filter(question = qn,vendor = yonghu).exists():
            temp = nonchoicequestion.objects.get(question = qn,vendor = yonghu)
            temp.is_active = not temp.is_active
            temp.save()
#        else:
#            return HttpResponse("sth wrong")            
        info = ["action","state","question"]
        schoicelist = [info]
        info = ["multi choice question"]
        mchoicelist = [info]
        info = ["text question"]
        textlist = [info]
        for q in yonghu.choicequestion_set.filter(questionnaire=shijian.questionnaire).all():
            temp = "temp"
            if not q.is_active:
                temp = "finalized"
            else:
                temp = "active   "            
            if q.multi_choice:
                mchoicelist.append([temp,q.question])
            else:
                schoicelist.append([temp,q.question])
        for q in yonghu.nonchoicequestion_set.filter(questionnaire=shijian.questionnaire).all():
            if not q.is_active:
                temp = "finalized"
            else:
                temp = "active   " 
            textlist.append([temp,q.question])
        for user in shijian.guest_event.all():
            schoicelist[0].append(user.username)
            i=1
            j=1
            for q in yonghu.choicequestion_set.filter(questionnaire=shijian.questionnaire).all():
                if q.multi_choice:
                    if user.answersheet_set.filter(questionnaire=shijian.questionnaire).exists():
                        answersheet = user.answersheet_set.get(questionnaire=shijian.questionnaire)
                        if answersheet.multichoiceanswer_set.filter(question = q).exists():
                            answers = answersheet.multichoiceanswer_set.filter(question = q).all()
                            ans=''
                            for answer in answers:
                                ans=ans+answer.choices.get().description+';'
                            mchoicelist[j].append(ans)
                    else:
                        mchoicelist[j].append("NOT ANSWER YET")
                    ++j
                else:
                    if user.answersheet_set.filter(questionnaire=shijian.questionnaire).exists():
                        answersheet = user.answersheet_set.get(questionnaire=shijian.questionnaire)
                        if answersheet.singlechoiceanswer_set.filter(question = q).exists():
                            answer = answersheet.singlechoiceanswer_set.get(question = q).choice.description
                            schoicelist[i].append(answer) 
                    else:
                        schoicelist[i].append("NOT ANSWER YET") 
                    ++i                    
            i=1
            for q in yonghu.nonchoicequestion_set.filter(questionnaire=shijian.questionnaire).all():
                if user.answersheet_set.filter(questionnaire=shijian.questionnaire).exists():
                    answersheet = user.answersheet_set.get(questionnaire=shijian.questionnaire)
                    if answersheet.textanswer_set.filter(question = q).exists():
                        answer = answersheet.textanswer_set.get(question = q).text
                        textlist[i].append(answer)
                else:
                    textlist[i].append("NOT ANSWER YET")
                ++i
        return render(request,'event/event_detail_vendor.html',context={'ini':schoicelist[0],'sl':schoicelist[1:],'ml':mchoicelist[1:],'tl':textlist[1:],'event_info':shijian,'choiceq':xuanze,'textq':wenda})
    else:
        return render(request,'users/realuser1.html')


"""
def addQuestion(request):
    pk = request.GET.get('p1')
    if request.method == "POST":
        event = Event.objects.get(id = pk)
        A = Question()
        A.question_content = request.POST['question']
        A.question_answer = ''
        A.Event = event
        A.save()
        return HttpResponse("Successfull add your question!")
    else:
        return HttpResponse("Fail to add your question")

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
    return render(request, 'event/addText.html', context={'event_info': shijian, 'user': yonghu})

def addOption(request):
    pk1 = request.GET.get('p1')
    pk2 = request.GET.get('p2')
    shijian = Event.objects.get(id = pk1)
    question = QuestionMultiple.objects.get(id = pk2)
    return render(request, 'event/addOption.html', context={'event_info': shijian, 'question' : question})

def addOptionA(request):
    pk1 = request.GET.get('p1')
    pk2 = request.GET.get('p2')
    if request.method == "POST":
        event = Event.objects.get(id = pk1)
        A = QuestionMultiple.objects.get(id = pk2)
        A.Choice.append(request.POST['option'])
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
"""