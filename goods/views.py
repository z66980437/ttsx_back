from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from goods.models import GoodsCategory, Goods


def category(request):
    if request.method == 'GET':
        category = GoodsCategory.objects.filter(pk=1).first()
        return render(request,'goods_category_detail.html',{'category_image':category.category_front_image,'category_id':category.id})

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        if category_id:
            category = GoodsCategory.objects.filter(pk=category_id).first()
            print(category.category_front_image)
            return JsonResponse({'code': 200, 'msg': '请求成功', 'category_image':str(category.category_front_image)})
        category = request.POST.get('category')
        files = request._files.get('category_front_image')

        allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
        file_suffix = files.name.split(".")[-1]
        if file_suffix not in allow_suffix:
            return JsonResponse({"error": 1, "message": "图片格式不正确"})
        path_name = './static/images/banner0'+category+'.'+file_suffix
        with open(path_name, 'wb') as f:
            f.write(files.file.read())

        category = GoodsCategory.objects.filter(pk=category).first()
        return render(request,'goods_category_detail.html',{'category_image':category.category_front_image,'category_id':category.id})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def goods_list(request,page):
    if request.method == 'GET':
        all_goods = Goods.objects.all()
        paginator = Paginator(all_goods,10)

        try:
            goods_list = paginator.page(int(page))
        except PageNotAnInteger:
            goods_list = paginator.page(1)
        except EmptyPage:
            goods_list = paginator.page(paginator.num_pages)

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
        return render(request,'goods_list.html',{'goods_list':goods_list,'page':page,'page_list':page_list,'max_page':paginator.num_pages})


def add_goods(request):
    if request.method == 'GET':
        return render(request,'goods_detail.html')
    if request.method == 'POST':
        goods_name = request.POST.get('name')
        goods_sn = request.POST.get('goods_sn')
        category_id = request.POST.get('category_id')
        goods_nums = request.POST.get('goods_nums')
        market_price = request.POST.get('market_price')
        shop_price = request.POST.get('shop_price')
        goods_brief = request.POST.get('goods_brief')
        upload_method = request.POST.get('upload_method')
        image_url = request.POST.get('image_url')
        goods_desc = request.POST.get('goods_desc')
        # 本地图片上传
        if upload_method == '1':
            files = request._files.get('goods_front_image')
            allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
            file_suffix = files.name.split(".")[-1]
            if file_suffix not in allow_suffix:
                return JsonResponse({"error": 1, "message": "图片格式不正确"})
            # 尝试存储商品资料
            try:
                Goods.objects.create(name=goods_name,
                                     goods_sn=goods_sn,
                                     goods_nums=goods_nums,
                                     market_price=market_price,
                                     shop_price=shop_price,
                                     goods_brief=goods_brief,
                                     goods_desc=goods_desc,
                                     goods_front_image='/static/images/goods_sn='+ goods_sn+ '.' + file_suffix,
                                     category_id=category_id)
            except:
                return JsonResponse({"error": 1, "message": "商品内容不正确"})
            #存储商品首图
            path_name = './static/images/goods_sn=' + goods_sn + '.' + file_suffix
            with open(path_name, 'wb') as f:
                f.write(files.file.read())
        #网络图片
        elif upload_method == '2':
            allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
            file_suffix = image_url.split(".")[-1]
            if file_suffix not in allow_suffix:
                return JsonResponse({"error": 1, "message": "图片格式不正确"})
            try:
                Goods.objects.create(name=goods_name,
                                     goods_sn=goods_sn,
                                     goods_nums=goods_nums,
                                     market_price=market_price,
                                     shop_price=shop_price,
                                     goods_brief=goods_brief,
                                     goods_desc=goods_desc,
                                     goods_front_image=image_url,
                                     category_id=category_id)
            except:
                return JsonResponse({"error": 1, "message": "商品内容不正确"})
        return JsonResponse({'code':200,'message':'添加商品成功!'})


def edit_goods(request,goods_id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=goods_id).first()
        return render(request,'goods_edit.html',{'goods':goods})
    if request.method == 'POST':
        goods = Goods.objects.filter(pk=goods_id).first()
        goods.name = request.POST.get('name')
        goods.goods_sn = request.POST.get('goods_sn')
        goods.category_id = request.POST.get('category_id')
        goods.goods_nums = request.POST.get('goods_nums')
        goods.market_price = request.POST.get('market_price')
        goods.shop_price = request.POST.get('shop_price')
        goods.goods_brief = request.POST.get('goods_brief')
        upload_method = request.POST.get('upload_method')
        image_url = request.POST.get('image_url')
        goods.goods_desc = request.POST.get('goods_desc')
        # 本地图片上传
        if upload_method == '1':
            files = request._files.get('goods_front_image')
            if files:
                allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
                file_suffix = files.name.split(".")[-1]
                if file_suffix not in allow_suffix:
                    return JsonResponse({"error": 1, "message": "图片格式不正确"})
                goods.goods_front_image = '/static/images/goods_id=' + goods_id + '.' + file_suffix,
            # 尝试存储商品资料
            try:
                goods.save()
            except:
                return JsonResponse({"error": 1, "message": "商品内容不正确"})
            # 存储商品首图
            if files:
                path_name = './static/images/goods_id=' + goods.id + '.' + file_suffix
                with open(path_name, 'wb') as f:
                    f.write(files.file.read())
        #网络图片上传
        elif upload_method == '2':
            if image_url:
                allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
                file_suffix = image_url.split(".")[-1]
                if file_suffix not in allow_suffix:
                    return JsonResponse({"error": 1, "message": "图片格式不正确"})
                goods.goods_front_image = image_url
            try:
                goods.save()
            except:
                return JsonResponse({"error": 1, "message": "商品内容不正确"})
        return JsonResponse({'code': 200, 'message': '商品信息保存成功!'})

import os
def remove_goods(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods = Goods.objects.filter(pk=goods_id).first()
        if str(goods.goods_front_image)[0:15] == '/static/images/':
            os.remove('.'+str(goods.goods_front_image))
        goods.delete()

        return JsonResponse({'code':200,'msg':'删除成功'})
