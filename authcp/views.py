from django.shortcuts import render


def index(request):
    return render(request, "authcp/index.html", {})

def login(request):
    return render(request, "authcp/login.html", {})