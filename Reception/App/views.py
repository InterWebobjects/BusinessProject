from alipay import AliPay
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader, Context
from django.urls import reverse

from App.models import *
from cart.cart import Cart

from Reception.settings import DEFAULT_FROM_EMAIL, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY, ALI_APP_ID


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

        alipay = AliPay(
            appid=ALI_APP_ID,
            app_notify_url=None,
            app_private_key_string=APP_PRIVATE_KEY,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,
            sign_type="RSA2",
            debug=False
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no="{}".format(newOrder.number),
            total_amount=newOrder.money,
            subject=newOrder.number,
            return_url="http://127.0.0.1/finish/?id=" + str(newOrder.id),
            notify_url="http://127.0.0.1/orders/",

        )
        net = "https://openapi.alipaydev.com/gateway.do?{}".format(order_string)
        return redirect(net)

    return redirect(reverse('app:index'))


def finish(request):
    oid = request.GET.get('id')
    if oid:
        order_pay = Order.objects.get(id=int(oid))
        order_pay.pay_time = datetime.now()
        order_pay.save()
    return redirect(reverse('app:emptyitems'))


def repay(request):
    newOrder = Order.objects.get(id=request.GET.get('oid'))
    alipay = AliPay(
        appid=ALI_APP_ID,
        app_notify_url=None,
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA2",
        debug=False
    )
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="{}".format(newOrder.number),
        total_amount=newOrder.money,
        subject=newOrder.number,
        return_url="http://49.234.99.134/finish/?id=" + str(newOrder.id),
        notify_url="http://49.234.99.134/orders/",

    )
    net = "https://openapi.alipaydev.com/gateway.do?{}".format(order_string)
    return redirect(net)


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
        context = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'message': request.POST.get('message'),
        }
        html_content = loader.get_template('mail.html').render(context)
        msg = EmailMultiAlternatives('Customer feedback', html_content, DEFAULT_FROM_EMAIL, ['kornchn@outlook.com'])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    styles = styleList(request)
    return render(request, 'contact.html', locals())


def confirm(request):
    order_id = request.GET.get('id')
    order_confirm = Order.objects.get(id=int(order_id))
    order_confirm.receive_time = datetime.now()
    order_confirm.save()
    return redirect(reverse('app:orders'))


@login_required
def newpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        print(old_password, new_password, re_password)
        user = User.check_login(email=email, password=old_password)
        if user and new_password == re_password:
            user.password = new_password
            user.save()
            return redirect(reverse('app:account'))
    styles = styleList(request)
    return render(request, 'password.html', locals())


@login_required
def info(request):
    if request.method == 'POST':
        user_info = User.objects.get(uid=request.POST.get('uid'))
        if request.POST.get('first_name'):
            user_info.first_name = request.POST.get('first_name')
        if request.POST.get('last_name'):
            user_info.last_name = request.POST.get('last_name')
        if request.POST.get('mobile'):
            user_info.mobile = request.POST.get('mobile')
        user_info.address = request.POST.get('address')
        user_info.gender = request.POST.get('gender')
        user_info.save()
    user = User.objects.get(uid=request.user.uid)
    styles = styleList(request)
    return render(request, 'info.html', locals())
