from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username} you are now officially registered!')
            return redirect('users:login')
        else:
            print(form.error_messages)
    form = RegisterForm()
    return render(request,'users/register.html',{'form':form})


def logout_view(request):
    logout(request)
    return render(request,"myapp/logout.html",{})

@login_required
def profile_view(request):
    return render(request,'users/profile.html')
