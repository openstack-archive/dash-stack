import random, hashlib, datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import User

from .forms import UserRegisterForm
from user_profile.models import Profile

# email sending function
def send_email(con,subject,email_to,email_from):
    c = Context(con)
    text_content = render_to_string('mail/user_register_welcome.txt', c)
    html_content = render_to_string('mail/user_register_welcome.html', c)

    email = EmailMultiAlternatives(subject,text_content,email_from)
    email.attach_alternative(html_content, "text/html")
    email.to = [email_to]
    email.send()

def index(request):
    return render(request, "authcp/index.html", {})

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            u=User.objects.create_user(
                form.cleaned_data['email'],
                form.cleaned_data['email'],
                form.cleaned_data['password2'],
            )
            u.is_active=False
            u.save()
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt=form.cleaned_data['email']
            profile=Profile.objects.get(user_id=u.id)
            profile.activation_key=hashlib.sha1(salt+usernamesalt).hexdigest()
            profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2),
                                                                "%Y-%m-%d %H:%M:%S")
            profile.save()
            send_email({'u': u, 'profil': profile},
                       'Welcome to our cloud',
                       u.email,
                       settings.DEFAULT_EMAIL_FROM,
                       )
            return render(request,
                          'authcp/success.html',
                          {'u': u, 'profil': profile})
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'authcp/register.html', {'form': form})

def register_success(request):
    return render(request, 'authcp/success.html', {})

def activation(request, key):
    activation_expired=False
    already_active=False
    profile=get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            # Display: offer the user to send a new activation link
            activation_expired=True
            id_user=profile.user.id
        # Activation successful
        else:
            profile.user.is_active=True
            profile.user.save()
    # If user is already active, simply display error message
    else:
        # Display : error message
        already_active=True
    return render(request, 'authcp/activation.html', locals())