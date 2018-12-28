import re

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from user.models import Admin


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # TODO: 判断某些页面需要登录才能访问，某些也许不需要登录就可以访问
        # TODO：需要登录的页面，当用户没有登录时，该如何处理？
        # 给request.user赋值，赋的值为当前登录系统的用户对象
        admin_id = request.session.get('admin_id')
        if admin_id:
            admin = Admin.objects.filter(pk=admin_id).first()
            request.admin = admin
            # 可以访问所有的页面
            return None
        not_need_path = ['/admin/login/']
        path = request.path
        for not_path in not_need_path:
            # 匹配当前路径是否为不需要登录验证的路径
            if re.match(not_path, path):
                return None
        # 当前的请求url不在not_need_path中，则表示当前url需要登录才能访问
        return HttpResponseRedirect(reverse('admin:login'))