from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.



def loginView(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            #form=AuthenticationForm()
            #return render(request, "registration/login.html", {'form':form})
            return HttpResponse('Invalid user')
    else:
        form=AuthenticationForm()
        return render(request, "registration/login.html", {'form':form})


def logoutView(request):
    logout(request)
    return redirect('index')

def registerView(request):
    if request.method == "POST":
        form=UserCreationForm(request.POST)
        if(form.is_valid()):
            username=request.POST['username']
            password1=request.POST['password1']
            password2=request.POST['password2']
            user = User.objects.create_user(username=username,email=None,password=password1)
            user.save()
            userlog = authenticate(request,username=username, password=password1)
            login(request,userlog)
            return redirect('index')
        else:
            return HttpResponse('Credentials are not valid go back and enter again')
    else:
        form=UserCreationForm()
        return render(request, "registration/register.html", {"form":form})
