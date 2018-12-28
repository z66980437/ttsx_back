
from django.conf.urls import url

from goods import views

urlpatterns = [

    # 商品分类
    url(r'^category/', views.category, name='category'),

    # 商品列表
    url(r'^goods_list/(\d+)/', views.goods_list, name='goods_list'),
    # 添加商品
    url(r'^add_goods/', views.add_goods, name='add_goods'),
    # 编辑商品
    url(r'^edit_goods/(\d+)/', views.edit_goods, name='edit_goods'),
    # 删除商品
    url(r'^remove_goods/', views.remove_goods, name='remove_goods'),

]

