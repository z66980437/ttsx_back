from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse


from order.models import OrderGoods, OrderInfo
from user.models import UserAddress
from goods.models import Goods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def order_list(request,page):
    if request.method == 'GET':
        all_orders = OrderInfo.objects.all()
        paginator = Paginator(all_orders, 10)

        try:
            orders_list = paginator.page(int(page))
        except PageNotAnInteger:
            orders_list = paginator.page(1)
        except EmptyPage:
            orders_list = paginator.page(paginator.num_pages)
        page = int(page)
        if paginator.num_pages < 8:
            page_list = range(1,paginator.num_pages+1)
        else:
            if page <= 3:
                page_list = range(1,8)
            elif page >= paginator.num_pages - 2:
                page_list = range(paginator.num_pages - 5, paginator.num_pages+1)
            else:
                page_list = range(page - 3,page + 4)
        return render(request,'order_list.html',{'orders':orders_list,'page':page,'page_list':page_list,'max_page':paginator.num_pages})