from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import registrationform
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def homepage(request):
    return render(request,"homepage.html",{
                "username": request.user,
            })
def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return render(request,"homepage.html",{
                "username": user.username,
            })
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username Doesn't Exist")
            else:
                messages.info(request, "Incorrect Password")
            return redirect('/')
    else:  
       return render(request, "login.html")
def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method=='POST':
        form = registrationform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'Hello {username}, You are Successfully Registered!!') 
            return render(request, 'login.html',)
    else:
        form = registrationform()
    return render(request, 'register.html', {'form':form})