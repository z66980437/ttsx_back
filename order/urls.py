
from django.conf.urls import url

from order import views

urlpatterns = [
    # 订单列表
    url(r'^order_list/(\d+)/', views.order_list, name='order_list'),

]

