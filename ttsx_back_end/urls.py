"""ttsx_back_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

urlpatterns = [
    # 用户界面
    url(r'^admin/', include('user.urls',namespace='admin')),
    # 商品管理
    url(r'^admin_goods/', include('goods.urls',namespace='admin_goods')),
    # 订单管理
    url(r'^admin_order/', include('order.urls',namespace='admin_order')),
]
