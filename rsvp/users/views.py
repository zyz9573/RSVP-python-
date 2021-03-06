from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import RegisterForm
from .models import realuser
def register(request):
    #only when we get a POST request, we need to get the information user submit
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request,'users/register.html',context={'form':form})
            
def index(request):
    return render(request,'index.html')

def detail(request):
    if not request.user.is_authenticated:
        return render(request,'index.html')
    else:
        pk = request.user.id
        yonghu = realuser.objects.get(id = pk)
        as_owner = yonghu.owner_event.all()
        as_vendor = yonghu.vendor_event.all()
        as_guest = yonghu.guest_event.all()
        return render(request,'users/realuser1.html',context={'user_info':yonghu,'owner':as_owner,'vendor':as_vendor,'guest':as_guest})#HttpResponse(yonghu.username)

