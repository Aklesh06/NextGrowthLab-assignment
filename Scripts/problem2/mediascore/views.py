from django.shortcuts import render,redirect
from .models import AndroidApp, RegisterUser, ClientInfo
from django.contrib import messages
from .forms import AndroidAppForm, RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import os
from django.conf import settings

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST,request.FILES)
        if(form.is_valid()):
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if RegisterUser.objects.filter(username=username).exists():
                messages.info(request, "Email Already Exists")
                return redirect('register')
            user = RegisterUser.objects.create_user(username= username,email= email, password= password)
            user.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html',{'form':form})
 
def login(request):
    if(request.user.is_anonymous == False):
        if(request.user.is_admin):
            return redirect('adminHome')
        else:
            return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        print(username,password)
        user = authenticate(request, username = username, password = password)
        if RegisterUser.objects.filter(username = username).exists():
            print('Authenticate not working')
        
        if user is not None:
            auth_login(request, user)
            if(user.is_admin == True):
                return redirect('adminHome')
            else:
                return redirect('home')
        else:
            messages.info(request,'Invalid Username/Password')
            return redirect('login')
    else:    
        return render(request, 'login.html')
    
def logout(request):
    auth_logout(request)
    return redirect('/')

def home(request):
    if request.user.is_anonymous:
        return redirect('login')
    user = request.user
    all_app = AndroidApp.objects.all()
    
    clientdata, created = ClientInfo.objects.get_or_create(
            username = user.username,
            defaults={
                'screenShot':[],
                'appNames':[],
                'totalPoints' : 0,
            }
        )
    return render(request, 'home.html',{'all_app':all_app, 'user':user, 'clientinfo':clientdata})

def tasks(request):
    if request.user.is_anonymous:
        return redirect('login')
    user = request.user
    all_app = AndroidApp.objects.all()
    clientdata = ClientInfo.objects.get(username = user.username)
    totalapp = 0
    for app in all_app:
        totalapp+=1
    
    return render(request, 'task.html',{'all_app':all_app, 'user':user, 'clientinfo':clientdata, 'totalapp':totalapp})

def adminHome(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.user.is_admin:
        user = request.user
        all_app = AndroidApp.objects.all()
        totalapp = 0
        for app in all_app:
            totalapp+=1
        return render(request, 'adminHome.html',{'all_app':all_app, 'user':user, 'totalapp':totalapp})
    else:
        return redirect('login')

def add_adroidApp(request):
    if request.user.is_anonymous:
        return redirect('login')
    if (request.user.is_admin): 
        if request.method == 'POST':
            form = AndroidAppForm(request.POST,request.FILES)
            if(form.is_valid):
                form.save()
                return redirect('adminHome')
        else:
            form = AndroidAppForm()

        return render(request ,'admin.html',{'form':form})
    else:
        return redirect('login')
    
def claimpoint(request,appid):
    if request.user.is_anonymous:
        return redirect('login')
    
    user = request.user
    appdetail = AndroidApp.objects.get(id = appid)
    if request.method == 'POST':
        img_presence = False
        if 'icon' in request.FILES:
            screenshot = request.FILES['icon']
            img_presence = True
        appname = appdetail.appName
        apppoint = appdetail.points
        username = user.username
        
        clientdata, created = ClientInfo.objects.get_or_create(
            username = username,
            defaults={
                'screenShot':[],
                'appNames':[],
                'totalPoints' : 0,
            }
        )
        if img_presence:
            file_path = os.path.join(settings.MEDIA_ROOT, 'screenshots', screenshot.name)
            with open(file_path, 'wb+') as destination:
                for part in screenshot.chunks():
                    destination.write(part)

            clientdata.screenShot.append(f'screenshots/{screenshot.name}')
        clientdata.totalPoints = clientdata.totalPoints + apppoint 
        clientdata.appNames.append(appname)
        clientdata.save()
        
        return redirect('tasks')
        
    return render(request, 'claim.html',{'appdetail':appdetail, 'user':user})
        
def points(request):
    if request.user.is_anonymous:
        return redirect('login')
    user = request.user
    clientinfo = ClientInfo.objects.get(username = user.username)
    
    return render(request, 'points.html', {'clientinfo':clientinfo})        
        
def profile(request):
    if request.user.is_anonymous:
        return redirect('login')
    user = request.user
    return render(request, 'profile.html', {'user':user})


        
