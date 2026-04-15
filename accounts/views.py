
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully!")
            return redirect('login')
        else:
            messages.error(request,"Invalid data ! account already exists.")
    else:
            form=UserCreationForm()
    return render(request,'accounts/register.html',{
                "form": form
            })
def login_user(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('dashboard_overview')  
            else:
                return redirect('home')         

        else:
            from django.contrib import messages
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")
   
def logout_user(request):
    logout(request)
    return redirect('home')
