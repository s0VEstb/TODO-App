import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .models import SMScode, Profile
from .forms import RegisterForm, SMScodeForm, LoginForm

# Create your views here.
def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request,
                      'user_handler/register.html',
                      context={'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request,
                          'user_handler/register.html',
                          context={'form': form})
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            is_active=False
        )
        profile = Profile.objects.create(
            user=user,
            image=form.cleaned_data['image'],
            bio=form.cleaned_data['bio'],
            age=form.cleaned_data['age']
        )
        code = ''.join([str(random.randint(0, 9)) for i in range(4)])
        SMScode.objects.create(
            code=code,
            user=user
        )
        send_mail(
            'Your code',
            message=code,
            from_email='<EMAIL>',
            recipient_list=[user.email]
        )
        return redirect("/confirm_sms/")


def confirm_sms_view(request):
    if request.method == 'GET':
        form = SMScodeForm()
        return render(request,
                      'user_handler/confirm_sms.html',
                      context={'form': form})
    elif request.method == 'POST':
        form = SMScodeForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request,
                          'user_handler/confirm_sms.html',
                          context={'form': form})

        sms = form.cleaned_data['SMS']
        code = SMScode.objects.filter(code=sms).first()

        if not code:
            form.add_error(None, 'Invalid code')
            return render(request,
                          'user_handler/confirm_sms.html',
                          context={'form': form})

        code.user.is_active = True
        code.user.save()
        code.delete()

        return redirect("/tasks")


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,
                      'user_handler/login.html',
                      context={'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request,
                          'user_handler/login.html',
                          context={'form': form})
        authenticated_user = authenticate(username=form.cleaned_data['username'],
                                          password=form.cleaned_data['password'])
        if not authenticated_user:
            form.add_error(None, 'Invalid username or password')
            return render(request,
                          'user_handler/login.html',
                          context={'form': form})
        login(request, authenticated_user)
        return redirect("/tasks")


@login_required
def profile_view(request):
    if request.method == 'GET':
        tasks = request.user.tasks.all()
        print(tasks)
        return render(request,
                      'user_handler/profile.html',
                      {'tasks': tasks})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/tasks/')






