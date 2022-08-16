from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.views import View

from .models import User

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username is already in use')
            return render(request, 'register.html')
        else:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            messages.success(request, 'register success')
            return redirect('user:login')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'login success')
            return redirect('index')
        else:
            messages.error(request, 'login error')
            return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'logout success')
    return redirect('index')
