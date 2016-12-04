from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User

from .forms import UserRegisterForm

def index(request):
    return render(request, "authcp/index.html", {})

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User()
            user.username=form.cleaned_data['email']
            user.email=form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect('/auth/register-success/')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'authcp/register.html', {'form': form})

def register_success(request):
    return render(request, 'authcp/success.html', {})