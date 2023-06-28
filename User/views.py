import sre_constants
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
import requests
import uuid
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
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.views.generic.base import ContextMixin
from django.http import FileResponse
from rest_framework.renderers import JSONRenderer

import base64


def get_basic_auth_str(username, password):
    temp_str = username + ':' + password
    # 转成bytes string
    bytesString = temp_str.encode(encoding="utf-8")
    # base64 编码
    encodestr = base64.b64encode(bytesString)
    # 解码
    decodestr = base64.b64decode(encodestr)
    return 'Basic ' + encodestr.decode()


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
            if username == "admin":
                user = authenticate(request, username=username, password=password, model=UserInfo)

                if user is not None:
                    # 如果验证通过，生成一个 Token 并返回给前端
                    token = generate_token(user)
                    return JsonResponse({'token': token, 'position': user.position, 'username': user.username,
                                         'user_uuid': user.user_uuid})
                else:
                    # 如果验证失败，返回错误信息
                    # return Response('Invalid credentials')
                    return JsonResponse({'error': 'Invalid credentials'}, status=400)
            else:

                # 设置Crowd服务器的URL和应用程序信息
                url = settings.CROWD_OPTIONS['crowd_serve_ip'] + '/crowd/rest/usermanagement/1/session'
                # 设置HTTP头信息，包括应用程序信息和返回的数据类型
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': get_basic_auth_str(settings.CROWD_OPTIONS['application_name'],
                                                        settings.CROWD_OPTIONS['application_password'])
                }
                data = {
                    "username": request.data.get('username'),
                    "password": request.data.get('password'),
                    "validation-factors": {
                        "validationFactors": [
                            {
                                "name": "remote_address",
                                "value": settings.CROWD_OPTIONS['local_ip']
                            }
                        ]
                    }
                }

                # 发出HTTP GET请求，获取所有用户信息
                # response = requests.get(url, headers=headers)
                response = requests.post(url, json=data, headers=headers)
                # 解析返回的JSON数据
                crowd_response = response.json()
                queryset = UserInfo.objects.filter(username=request.data.get('username'))
                if crowd_response['token']:
                    user = authenticate(request, username=username, password=password, model=UserInfo)
                    if user is not None:
                        return JsonResponse(
                            {'token': crowd_response['token'], 'position': user.position, 'username': user.username,
                             'user_uuid': user.user_uuid})
                    elif queryset.count() != 0:
                        queryset[0].set_password(request.data.get('password'))
                        queryset[0].save()
                        return JsonResponse(
                            {'token': crowd_response['token'], 'position': queryset[0].position, 'username': crowd_response['user']['name'],
                             'user_uuid': queryset[0].user_uuid})
                    else:
                        UserManager.create_user(self, username=request.data.get('username'),
                                                password=request.data.get('password'),
                                                user_uuid=str(uuid.uuid4()),
                                                create_date=datetime.now().strftime('%Y-%m-%d'),
                                                position='read').save()
                        return JsonResponse({'token': crowd_response['token'], 'position': 'read',
                                             'username': crowd_response['user']['name'],
                                             'user_uuid': request.data.get('user_uuid')})
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
        # 1.当前用户所有的权限
        from django.conf import settings
        permission_dict = settings.PERMISSIONS[request.user.role]

        # 2.当前用户正在访问的url和方式
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


def download_help_docx(*args, **kwargs):
    # 检查文件是否存在
    if not os.path.exists("doc/RegStudio使用文档.docx"):
        # 如果文件不存在，返回适当的错误响应
        return Response(status=404)

    # 通过FileResponse发送文件响应
    response = FileResponse(open("doc/RegStudio使用文档.docx", 'rb'),
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="your-docx-file.docx"'
    return response