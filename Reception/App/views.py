from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import *
from cart.cart import Cart

from Reception.settings import EMAIL_HOST_USER


def styleList(request):
    styleMan = Style.objects.filter(Q(sid__lt=4) | Q(sid=6) | Q(sid=7))
    styleWomen = Style.objects.filter(sid__lt=6)
    styleClassic = Style.objects.filter(sid__gt=7)
    styleAll = Style.objects.all()
    cartPicture = Cart(request)
    return styleMan, styleWomen, styleClassic, styleAll, cartPicture


def index(request):
    styles = styleList(request)
    aboutList = Commodity.objects.order_by('-id')[0:3]
    productList = Commodity.objects.order_by('-id')[3:11]

    return render(request, 'index.html', locals())


def product(request, sid, tag=2):
    sid = int(sid)
    tag = int(tag)
    if tag != 2:
        productList = Commodity.objects.filter(sid=sid, tag=tag)
    else:
        productList = Commodity.objects.filter(sid=sid)
    styles = styleList(request)
    return render(request, 'products.html', locals())


def account(request):
    next = request.GET.get('next', None)
    if request.method == 'POST':
        next = request.POST.get('next')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.check_login(email=email, password=password)
        if user:
            login(request, user)
            if next == 'None':
                return redirect(reverse('app:index'))
            else:
                return redirect(next)
    styles = styleList(request)
    return render(request, 'account.html', locals())


def register(request):
    styles = styleList(request)
    return render(request, 'register.html', locals())


def cart(request):
    # cartList = Cart.objects.filter(uid=request.user.uid)
    # styles = styleList()
    # return render(request, 'checkout.html', locals())
    cartList = Cart(request)
    # template = get_template('cart.html')
    # html = template.render(context=locals(), request=request)
    styles = styleList(request)
    return render(request, 'checkout.html', locals())


def user_logout(request):
    logout(request)
    return redirect(reverse('app:index'))


def single(request, cid):
    commodity = Commodity.objects.get(id=int(cid))
    recommendList = Commodity.objects.order_by('-id')[0:3]
    styles = styleList(request)
    return render(request, 'single.html', locals())


def add_to_cart(request, cid):
    add_product = Commodity.objects.get(id=int(cid))
    personal_cart = Cart(request)
    personal_cart.add(add_product, add_product.price, 1)
    path = '/single/' + cid + '/'
    return redirect(path)


def remove_from_cart(request, cid):
    cid = int(cid)
    remove_product = Commodity.objects.get(id=cid)
    personal_cart = Cart(request)
    personal_cart.remove(remove_product)
    return redirect('/cart/')


def empty_from_cart(request):
    personal_cart = Cart(request)
    personal_cart.clear()
    if request.GET.get('path'):
        return redirect(request.GET.get('path'))
    return redirect('app:index')


@login_required
def sellteaccounts(request):
    styles = styleList(request)
    return render(request, 'settle.html', locals())


def pay(request):
    if request.method == 'POST':
        newOrder = Order()
        newOrder.number = datetime.now().strftime("%Y%m%d%H%M%S%f")
        newOrder.money = int(request.POST.get('summary')[0:-3])
        newOrder.create_time = datetime.now()
        newOrder.uid = request.user
        newOrder.receiver = request.POST.get('receiver')
        newOrder.address = request.POST.get('address')
        newOrder.mobile = request.POST.get('mobile')
        clist = ''
        idlist = request.POST.getlist('cid')
        for cid in idlist:
            c = cid + '/' + request.POST.get('quantity' + cid) + ','
            clist += c
        newOrder.clist = clist
        newOrder.save()
    return redirect(reverse('app:emptyitems'))


@login_required
def orders(request):
    orders = Order.objects.filter(uid=request.user.uid).order_by('-id')
    olist = []
    for order in orders:
        item_list = order.clist.split(',')[:-1]
        comlist = []
        for item in item_list:
            com = Commodity.objects.get(id=int(item[0]))
            num = int(item[-1])
            comlist.append((com, num, com.price * num))
        olist.append((order, comlist))
    styles = styleList(request)
    return render(request, 'orders.html', locals())


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print('send')
        send_mail(
            'From:' + name + '<' + email + '>',
            message,
            EMAIL_HOST_USER,
            ['kornchn@outlook.com'],
            fail_silently=False
        )
        print('finish')
    styles = styleList(request)
    return render(request, 'contact.html', locals())


def confirm(request):
    order_id = request.GET.get('id')
    order_confirm = Order.objects.get(id=int(order_id))
    order_confirm.receive_time = datetime.now()
    order_confirm.save()
    return redirect(reverse('app:orders'))
