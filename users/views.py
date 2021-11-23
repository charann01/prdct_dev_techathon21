from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm
from .models import TokenModel, UserModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import secrets
from django.core.mail import send_mail

# Create your views here.

@login_required(login_url='login')
def Home(request):
    student = None
    students = None
    if request.user.is_staff == True:
        return redirect("/admin")
    elif request.user.user_type == 'student':
        student = request.user
    else:
        students = UserModel.objects.filter(user_type='student')
    return render(request,"home.html",{
        'student':student,
        'students':students
    })



def UserRegisterView(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.pop('password')
            form.cleaned_data.pop('confirm_password')
            user = UserModel(**form.cleaned_data)
            user.set_password(password)
            if form.cleaned_data['user_type'] == 'admin':
                user.is_superuser = True
                user.is_staff = True
            user.save()
            return redirect('login')
    return render(request,'users/register.html',{
        'form':form
    })


def UserLoginView(request):
    form = LoginForm()
    print("here")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request,user)
                return redirect('home')
    return render(request,'users/login.html',{'form':form})


def UserLogoutView(request):
    logout(request)
    return redirect("home")


def send_reset_link(request):
    token = secrets.token_hex(16)
    if request.method == "POST":
        username = request.POST['username']
        user = UserModel.objects.get(username=username)
        token_obj = TokenModel(user=user,token=token)
        token_obj.save()
        send_mail('Password Reset Request',f'http://127.0.0.1:8000/users/reset-pass/{token}',
        'devtechathon@gmail.com',[user.email,])
        return redirect('home')
    return render(request,'users/send_reset_link.html',{})


def reset_password(request,token):
    token = TokenModel.objects.get(token=token)
    user = token.user
    print(user)
    if request.method == 'POST':
        password = request.POST['password']
        user.set_password(password)
        user.save()
        token.delete()
        return redirect('login')
    return render(request,'users/reset_pass.html',{})
