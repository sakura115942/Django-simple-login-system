from django.utils import timezone
import datetime
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, EmailVerifyRecord

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'email is already in use')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'username is already in use')
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()
            messages.success(request, 'register success')
            return redirect('user:login')

        return render(request, 'register.html')


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


class MessageLoginRequiredMixin(LoginRequiredMixin):

    login_url = 'user:login'
    permission_denied_message = 'You need to login first to continue'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(MessageLoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'


class UserListView(MessageLoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'


class UserActivationView(View):
    effective_time = datetime.timedelta(minutes=30)

    def get(self, request, code):
        record = EmailVerifyRecord.objects.filter(code=code).get()
        user = User.objects.filter(email=record.email).get()
        deadline = record.send_time + self.effective_time
        
        if timezone.now() > deadline:
            messages.error(request, 'verification code has expired')
        elif user.is_auth == True:
            messages.error(request, 'do not repeat verification')
        else:
            user.is_auth = True
            user.save()
            auth.login(request, user)
            messages.success(request, 'verification succeeded')
        
        return redirect('index')
