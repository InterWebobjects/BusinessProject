from datetime import datetime

from Backstage.settings import MDEIA_ROOT
from tools.fileupload import FileUpload
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from pyecharts import Bar

from App.models import User, Commodity, Style, Order


# 主页
def index(request):
    users = User.objects.all()

    return render(request, 'index.html', locals())


# 显示主页内容模板
def index_Desktop(request):
    return render(request, 'welcome.html')


# 订单
def welcome(request, page=1):
    uses = Order.objects.all()
    content = request.GET.get('page')
    pagetor = Paginator(uses, 5)
    pagetion = pagetor.page((page))

    return render(request, 'order-list.html', locals())


# 订单详情

def views_user(request, id):
    commodity = Order.objects.get(id=int(id))
    itemlist = commodity.clist.split(',')[:-1]
    comList = []

    for item in itemlist:
        com = Commodity.objects.get(id=(item[0]))
        num = int(item[-1])
        comList.append((com, num))

    return render(request, 'order_detail的副本.html', locals())


# 会员
def users(request):
    return render(request, 'studentdetail.html')


# 用户详情
def students_Add(request, page=1):
    uses = User.objects.all()
    isactive = User.objects.filter(is_active=0)
    content = request.GET.get('page')
    pagetor = Paginator(uses, 5)
    pagetion = pagetor.page(int(page))

    return render(request, 'member-list.html', locals())


# 用户删除
def add_user(request, page=1):
    if page == '':
        page = 1
    removelist = request.GET.get('data')
    if removelist:
        remove = removelist.split(',')
        for i in remove:
            rm = User.objects.get(uid=int(i))
            rm.is_active = 0
            rm.save()
    uses = User.objects.all()
    isactive = User.objects.filter(is_active=0)
    coms = User.objects.all()
    content = request.GET.get('page')
    pagetor = Paginator(coms, 5)
    pagetion = pagetor.page(int(page))

    return render(request, 'member-list.html', locals())


# 用户添加
def students_Del(request, page=1):
    if page == '':
        page = 1
    removelist = request.GET.get('data')
    if removelist:
        remove = removelist.split(',')
        for i in remove:
            rm = User.objects.get(uid=int(i))
            rm.is_active = 1
            rm.save()
    uses = User.objects.all()
    isactive = User.objects.filter(is_active=1)
    coms = User.objects.all()
    content = request.GET.get('page')
    pagetor = Paginator(coms, 5, 2)
    pagetion = pagetor.page(int(page))

    return render(request, 'member-del.html', locals())


# 分类
def category(request):
    return render(request, 'cate.html')


# 登录
def login(request):
    return render(request, 'login.html')


# 注册
def registered(request):
    if request.method == 'POST':
        emali = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        add = User()
        add.username = emali
        add.email = emali
        add.first_name = firstname
        add.last_name = lastname
        add.date_joined = datetime.now()
        if len(phone) == 11:
            add.mobile = phone
        if password == repassword:
            add.password = password
        add.save()

    return render(request, 'member-add.html')


# 商品
def commodity_list(request, page=1):
    coms = Commodity.objects.all()
    isdel = Commodity.objects.filter(is_delete=0)
    content = request.GET.get('page')
    pagetor = Paginator(coms, 5)
    pagetion = pagetor.page(int(page))
    return render(request, 'commodity_list.html', locals())


# 添加商品
def add_commodity(request):
    path = MDEIA_ROOT
    if request.method == 'POST':
        if request.POST.get('submit'):
            data = Commodity()
            watchtypes = request.POST.get('watchtype')
            file1 = request.FILES.get('file1')
            obj = FileUpload(file1, is_randomname=True)
            obj.upload(path)
            data.picture_1 = obj.file_name
            file2 = request.FILES.get('file2')
            obj = FileUpload(file2, is_randomname=True)
            obj.upload(path)
            data.picture_2 = obj.file_name
            file3 = request.FILES.get('file3')
            obj = FileUpload(file3, is_randomname=True)
            obj.upload(path)
            data.picture_3 = obj.file_name
            desc = request.POST.get('desc')
            data.price = request.POST.get('price')
            data.cname = request.POST.get('commodity')
            data.sku = request.POST.get('number')
            data.plate = request.POST.get('c1')
            data.case = request.POST.get('c2')
            data.gem = request.POST.get('c3')
            data.strap = request.POST.get('c4')
            data.tag = request.POST.get('shipping')
            data.sid = Style.objects.filter(sid=watchtypes).first()
            data.description = desc
            data.watch = request.POST.get('watch')
            data.save()

            return render(request, 'order-list.html')

    return render(request, 'order-add.html', locals())


def del_commodity(request, page=1):
    if page == '':
        page = 1
    coms = Commodity.objects.all()
    isdels = Commodity.objects.filter(is_delete=1)
    content = request.GET.get('page', 5)
    pagetor = Paginator(coms, 5)
    pagetion = pagetor.page(int(page))

    return render(request, 'commodity_del.html', locals())


# 批量删除
def batchdeletion(request, page=1):
    if page == '':
        page = 1
    removelist = request.GET.get('data')
    if removelist:
        remove = removelist.split(',')
        for i in remove:
            rm = User.objects.get(uid=int(i))
            rm.is_active = 0
            rm.save()
    uses = Commodity.objects.all()
    isactive = Commodity.objects.filter(is_delete=0)
    coms = Commodity.objects.all()
    content = request.GET.get('page')
    pagetor = Paginator(coms, 5)
    pagetion = pagetor.page(int(page))
    return render(request, 'commodity_list.html', locals())


# 批量恢复
def batchrestore(request, page=1):
    if page == '':
        page = 1
    removelist = request.GET.get('data')
    if removelist:
        remove = removelist.split(',')
        for i in remove:
            rm = User.objects.get(uid=int(i))
            rm.is_active = 0
            rm.save()
    uses = Commodity.objects.all()
    isactive = Commodity.objects.filter(is_delete=1)
    coms = Commodity.objects.all()
    content = request.GET.get('page')
    pagetor = Paginator(coms, 5)
    pagetion = pagetor.page(int(page))
    return render(request, 'commodity_del.html', locals())
