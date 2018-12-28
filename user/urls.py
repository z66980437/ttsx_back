
from django.conf.urls import url

from user import views

urlpatterns = [
    #登录
    url(r'^login/', views.login, name='login'),

    # 注销
    url(r'^logout/', views.logout, name='logout'),

    # 后台管理首页
    url(r'^index/', views.index, name='index'),

    # 用户管理
    url(r'^user_list/(\d+)/', views.user_list, name='user_list'),


]

