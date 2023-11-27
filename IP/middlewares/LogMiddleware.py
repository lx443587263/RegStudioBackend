# -*- coding:utf-8 -*-
"""
@File   : LogMiddleware.py
@Author : Python
@Date   : 2021/7/20 14:00
"""
import time
import json

from django.utils.deprecation import MiddlewareMixin

from IP.models import OpLogs, AccessTimeOutLogs
from IP.sers import OpLogsSerializer, AccessTimeOutLogsSerializer


class opLogs(MiddlewareMixin):
    __exclude_urls = ['index/']  # 定义不需要记录日志的url名单

    def __init__(self, *args):
        super(opLogs, self, ).__init__(*args)
        self.start_time = None  # 开始时间
        self.end_time = None  # 响应时间
        self.data = {}  # dict数据

    def process_request(self, request):
        """
        请求进入
        :param request: 请求对象
        :return:
        """

        self.start_time = time.time()  # 开始时间
        re_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 请求时间（北京）
        # 请求IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # 如果有代理，获取真实IP
            re_ip = x_forwarded_for.split(",")[0]
        else:
            re_ip = request.META.get('REMOTE_ADDR')

        # 请求方法
        re_method = request.method

        if re_method != "GET":
            # 请求参数
            re_content = request.GET if re_method == 'GET' else request.POST
            if re_content:
                # 筛选空参数
                re_content = json.dumps(re_content)
                self.data.update(
                    {
                        're_time': re_time,  # 请求时间
                        're_url': request.path,  # 请求url
                        're_method': re_method,  # 请求方法
                        're_ip': re_ip,  # 请求IP
                        're_content': re_content,  # 请求参数
                        # 're_user': request.POST.get('username'),  # 操作人(需修改)，网站登录用户
                        're_user': 'AnonymousUser'  # 匿名操作用户测试
                    }
                )

    def process_response(self, request, response):
        """
        响应返回
        :param request: 请求对象
        :param response: 响应对象
        :return: response
        """
        # 请求url在 exclude_urls中，直接return，不保存操作日志记录
        if request.path in self.__exclude_urls:
            return response
        # for request.path in self.__exclude_urls:
        #     return response
            # if url in self.data.get('re_url'):
            #     return response

        # 获取响应数据字符串(多用于API, 返回JSON字符串)
        rp_content = response.content.decode()
        self.data['rp_content'] = rp_content

        # 耗时
        self.end_time = time.time()  # 响应时间
        access_time = self.end_time - self.start_time
        self.data['access_time'] = round(access_time * 1000)  # 耗时毫秒/ms

        # 耗时大于3s的请求,单独记录 (可将时间阈值设置在settings中,实现可配置化)
        if self.data.get('access_time') > 3 * 1000:
            AccessTimeOutLogs.objects.create(**self.data)  # 超时操作日志入库db

        # OpLogs.objects.all()
        if len(self.data['rp_content']) > 0:
            OpLogs.objects.create(**self.data)  # 操作日志入库db

        return response
