import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    return render(request, "base.html", {'time' : datetime.datetime.now()})