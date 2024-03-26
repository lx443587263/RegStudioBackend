from django.shortcuts import render
from PatternInfo.models import PatternInfo
from rest_framework.viewsets import ModelViewSet
from PatternInfo.sers import PatternInfoSerializers
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action, api_view
from rest_framework import status

# Create your views here.

class PatternInfoView(ModelViewSet):
    """IP视图"""
    queryset = PatternInfo.objects.all()
    serializer_class = PatternInfoSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_ = (
        "TEST_ITEM", "PATTERN_NAME", "TEST_CATEGORY", "TEST_PURPOSE", "TEST_PROCESS", "TEST_NOTES", "USER", "TIME",
        "RTL_VERSION", "NETLIST_VERSION", "SIM_MODE", "TOOL", "CORNER", "MTM", "SIM_SEED", "TWO_NODE", "MBIST",
        "FPGA_FLOW",
        "FPGA_WORK", "WORK_PATH", "LOG_NAME", "SIM_RESULTS", "CHECK_WAVE", "JTAG_ACCESS", "PATTERN_MD5",
        "PROJECT_NAME")  # 指定可搜索的字段
    filterset_fields = (
        "TEST_ITEM", "PATTERN_NAME", "TEST_CATEGORY", "TEST_PURPOSE", "TEST_PROCESS", "TEST_NOTES", "USER", "TIME",
        "RTL_VERSION", "NETLIST_VERSION", "SIM_MODE", "TOOL", "CORNER", "MTM", "SIM_SEED", "TWO_NODE", "MBIST",
        "FPGA_FLOW",
        "FPGA_WORK", "WORK_PATH", "LOG_NAME", "SIM_RESULTS", "CHECK_WAVE", "JTAG_ACCESS", "PATTERN_MD5", "PROJECT_NAME")


    def create(self, request, *args, **kwargs):
        data = request.data
        data.decode('utf-8')
        exists = PatternInfo.objects.filter(PATTERN_MD5=data.get('PATTERN_MD5')).exists()
        if exists:
            return Response({'error': '版本已存在'})
        return super().create(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        queryset = PatternInfo.objects.filter(PROJECT_NAME=request.GET.get('PROJECT_NAME')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

