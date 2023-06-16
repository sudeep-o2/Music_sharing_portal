from django.http import HttpResponse
from django.shortcuts import render,redirect
from . forms import MyUserCreationForm
from django.contrib.auth import authenticate, login,logout
from . models import MusicFile,User
from django.db.models import Q

# Create your views here.



def register(request):
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
            
    context={'form':form}
    return render(request,'base/login_reg.html',context)

def loginView(request):
    stat='login'
    if request.method=='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)
        except:
            return HttpResponse('error in email')
        
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse('Error')
    context={'stat':stat}
    return render(request,'base/login_reg.html',context)


def upload(request):
    if request.method == 'POST':
       
        MusicFile.objects.create(
            title = request.POST.get('title'),
            file = request.POST.get('file'),
            visibility = request.POST.get('visibility'),
            allowed_emails = request.POST.get('allowed_emails').split(','),     
        )
        return redirect('home')

    return render(request,'base/upload.html')
        
def home(request):

    user = request.user
    music_list = MusicFile.objects.filter(Q(visibility='public') | Q(visibility='private') | Q(visibility='protected',allowed_emails__contains=user))
    context={'user':user,'music_list':music_list}

    return render(request,'home.html',context)