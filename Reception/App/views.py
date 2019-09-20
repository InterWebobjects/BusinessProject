from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from App.models import *


def styleList():
    styleMan = Style.objects.filter(Q(sid__lt=4) | Q(sid=6) | Q(sid=7))
    styleWomen = Style.objects.filter(sid__lt=6)
    styleClassic = Style.objects.filter(sid__gt=7)
    return styleMan, styleWomen, styleClassic


def index(request):
    style = styleList()
    return render(request, 'index.html', locals())


def product(request, sid, tag=2):
    if tag != 2:
        productList = Commodity.objects.filter(sid=int(sid), tag=int(tag))
    style = styleList()
    return render(request, 'products.html')


def account(request):
    next = request.GET.get('next', None)
    if request.method == 'POST':
        next = request.POST.get('next')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.check_login(email=email, password=password)
        if user:
            login(request, user)
            if next != 'None':
                return redirect(next)
    return render(request, 'account.html', locals())


def register(request):
    return render(request, 'register.html')


@login_required
def cart(request):
    return render(request, 'checkout.html')


def logout(request):
    return render(request, 'single.html')


def single(request):
    return render(request, 'single.html')
