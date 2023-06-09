import sre_constants

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from User.models import UserInfo, UserManager
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from User.sers import UserInfoSerializers
import jwt
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.views.generic.base import ContextMixin
from rest_framework.renderers import JSONRenderer


def generate_token(user):
    # print(user)
    payload = {
        'user_uuid': user.user_uuid,
        'username': user.username,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         username = request.body.get('username')
#         password = request.POST.get('password')
#         print(username)
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'message': 'Success'})
#         else:
#             return JsonResponse({'message': 'Invalid credentials'})


class UserInfoView(ModelViewSet, ContextMixin):
    """RegGather视图"""
    model = UserInfo
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('user_uuid', 'username', 'password', 'position')  # 指定可搜索的字段
    filterset_fields = ('user_uuid', 'username', 'password', 'position')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('user_uuid'))
        queryset = UserInfo.objects.filter(user_uuid=request.GET.get('user_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = UserInfo.objects.get(user_uuid=request.GET.get('user_uuid'))

        if request.path == "/api/user/changePasswd/":
            new_password = request.data['new_password']
            queryset.set_password(new_password)
            queryset.save()
            # 返回密码修改成功的信息
            return Response('密码修改成功！')

        serializer = UserInfoSerializers(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @csrf_exempt
    def create(self, request):
        if request.method == 'POST':
            if request.path == "/api/user/add/":
                print(request.data)
                UserManager.create_user(self, username=request.data.get('username'),
                                        password=request.data.get('password'),
                                        user_uuid=request.data.get('user_uuid'),
                                        create_date=request.data.get('create_date'),
                                        position=request.data.get('position')).save()

            # return Response("hello")
            # 从 POST 请求中获取用户名和密码
            username = request.data.get('username')
            password = request.data.get('password')

            # queryset = UserInfo.objects.get(username=username)
            # 调用 Django 自带的 authenticate() 方法进行身份验证
            user = authenticate(request, username=username, password=password, model=UserInfo)

            if user is not None:
                # 如果验证通过，生成一个 Token 并返回给前端
                token = generate_token(user)
                return JsonResponse({'token': token, 'position': user.position, 'username': user.username, 'user_uuid': user.user_uuid})
            else:
                # 如果验证失败，返回错误信息
                # return Response('Invalid credentials')
                return JsonResponse({'error': 'Invalid credentials'}, status=400)


class MineAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 读取用户请求的token,检验是否合法
        token = request.query_params.get('token')
        token = request.query_params.get('role')
        if not token:
            raise exceptions.AuthenticationFailed("认证失败")
        return (None, None)

    def authenticate_header(self, request):
        return "User"


class MinPermission(BasePermission):
    def has_permission(self, request, view):
        print("判断权限", request.user.role)
        # 1.当前用户所有的权限
        from django.conf import settings
        permission_dict = settings.PERMISSIONS[request.user.role]

        # 2.当前用户正在访问的url和方式
        print(request.resolver_match.url_name, request.method)
        url_name = request.resolver_match.url_name
        method = request.method
        # 3.权限判断
        method_list = permission_dict.get(url_name)
        if not method_list:
            return False
        if method in method_list:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        return True
