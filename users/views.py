from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import RegisterForm
from .models import user
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

def detail(request,pk):
    yonghu = user.objects.get(id = pk)
    return HttpResponse(yonghu.username)