"""RegStudioBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from IP import views as IpViews
from User import views as UserViews
from PatternInfo import views as PatternInfoViews
from rest_framework import routers

# 注册路由
router = routers.DefaultRouter()
router.register('api/ip/ipinfo', IpViews.IpView)
router.register('api/ip/regGather', IpViews.RegGatherView)
router.register('api/ip/singleReg', IpViews.SingleRegView)
router.register('api/ip/value', IpViews.ValueView)
router.register('api/user/login', UserViews.UserInfoView)
router.register('api/user/add', UserViews.UserInfoView)
router.register('api/user/list', UserViews.UserInfoView)
router.register('api/user/changePasswd', UserViews.UserInfoView)
router.register('api/ip/upload_file', IpViews.FileViewSet)
router.register('api/ip/upload_template', IpViews.TemplateFileViewSet)
router.register('api/ip/ip_page_file', IpViews.IpPageFilesViewSet)
router.register('api/ip/category', IpViews.CategoryView)
router.register('api/ip/project', IpViews.ProjectView)
router.register('api/ip/modification', IpViews.modificationInfoView,basename='modification')
router.register('api/patterninfo',PatternInfoViews.PatternInfoView)
router.register('api/ip/projectchange',IpViews.ProjectChangeView)
router.register('api/ip/ModifyRecords',IpViews.ModifyRecordsView)
# router.register('api/ip/download_spec', IpViews.download_docx)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ip/download_spec/', IpViews.download_docx, name='download_spec'),
    path('api/ip/download_help/', UserViews.download_help_docx, name='download_help_spec'),
    path('api/ip/download_ip_page_file/', IpViews.download_docx, name='download_spec'),
    path('api/ip/modification/cut_page/', IpViews.cut_page),
    path('api/ip/ModifyRecords/cut_page/', IpViews.ModifyRecords_cut_page)

    # path('user/login', UserViews.login_view)
    # # 获取Token的接口
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # # 刷新Token有效期的接口
    # path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # # 验证Token的有效性
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path(r'^ipinfo/$', views.IpView.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destory'})),

    # path('ip/regGather', views.RegGatherView.as_view({"get": "list", "post": "create"})),
    # # url:publishes/1     get(request,pk=1)
    # re_path("ip/regGather/$",
    #         views.RegGatherView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
]

urlpatterns += router.urls
