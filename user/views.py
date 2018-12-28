from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from user.models import Admin


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        admin_name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        print(admin_name)
        print(pwd)
        # 验证完整性
        if not all([admin_name, pwd]):
            msg = '用户名或密码不全！'
            return render(request, 'login.html', {'msg_userpass': msg})
        admin = Admin.objects.filter(username=admin_name).first()
        # 判断用户是否存在
        if not admin:
            msg = '该用户不存在！'
            return render(request, 'login.html', {'msg_username': msg})

        print(make_password('123123'))
        # 验证密码正确性
        if check_password(pwd, admin.password):
            # django自带auth模块，签名token，会话上下文session
            request.session['admin_id'] = admin.id

            return HttpResponseRedirect(reverse('admin:index'))
        else:
            msg = '密码错误！'
            return render(request, 'login.html', {'msg_password': msg})


def logout(request):
    if request.method == 'GET':
        del request.session['admin_id']
        return HttpResponseRedirect(reverse('admin:login'))


def index(request):
    if request.method == 'GET':
        return render(request,'index.html')

from .models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def user_list(request,page):
    if request.method == 'GET':
        all_users = User.objects.all()
        paginator = Paginator(all_users, 10)

        try:
            users_list = paginator.page(int(page))
        except PageNotAnInteger:
            users_list = paginator.page(1)
        except EmptyPage:
            users_list = paginator.page(paginator.num_pages)
        page = int(page)
        if paginator.num_pages < 8:
            page_list = range(1, paginator.num_pages + 1)
        else:
            if page <= 3:
                page_list = range(1, 8)
            elif page >= paginator.num_pages - 2:
                page_list = range(paginator.num_pages - 5, paginator.num_pages + 1)
            else:
                page_list = range(page - 3, page + 4)
        return render(request,'user_list.html',{'users_list':users_list,'page':page,'page_list':page_list,'max_page':paginator.num_pages})