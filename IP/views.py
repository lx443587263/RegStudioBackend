from rest_framework.viewsets import ModelViewSet
from IP.models import IpInfo, RegGatherInfo, SingleRegInfo, ValueInfo
from IP.sers import IpSerializers, RegGatherSerializers, SingleRegSerializers, ValueSerializers
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class IpView(ModelViewSet):
    """IP视图"""
    queryset = IpInfo.objects.all()
    serializer_class = IpSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('ip_uuid',)  # 指定可搜索的字段
    filterset_fields = ('ip_uuid',)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('ip_uuid'))
        queryset = IpInfo.objects.filter(ip_uuid=request.GET.get('ip_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = IpInfo.objects.get(ip_uuid=request.GET.get('ip_uuid'))
        serializer = IpSerializers(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'version' in data:
            # 在数据库中查询是否存在相同的记录
            exists = IpInfo.objects.filter(ip_name=data.get('ip_name'), version=data.get('version')).exists()
            if exists:
                return Response({'error': 'IP版本已存在'})
        return super().create(request, *args, **kwargs)


class RegGatherView(ModelViewSet):
    """RegGather视图"""
    queryset = RegGatherInfo.objects.all()
    serializer_class = RegGatherSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('ip_uuid', 'tag', 'reg_gather_name', 'reg_gather_uuid')  # 指定可搜索的字段
    filterset_fields = ('ip_uuid', 'tag', 'reg_gather_name', 'reg_gather_uuid')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('reg_gather_uuid'))
        queryset = RegGatherInfo.objects.filter(reg_gather_uuid=request.GET.get('reg_gather_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = RegGatherInfo.objects.get(reg_gather_uuid=request.GET.get('reg_gather_uuid'))
        serializer = RegGatherSerializers(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class SingleRegView(ModelViewSet):
    """SingleReg视图"""
    queryset = SingleRegInfo.objects.all()
    serializer_class = SingleRegSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('reg_gather_uuid', 'single_reg_uuid')  # 指定可搜索的字段
    filterset_fields = ('reg_gather_uuid', 'single_reg_uuid')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        queryset = SingleRegInfo.objects.filter(single_reg_uuid=request.GET.get('single_reg_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = SingleRegInfo.objects.get(single_reg_uuid=request.GET.get('single_reg_uuid'))
        print(request.data)
        serializer = SingleRegSerializers(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def create(self, request, *args, **kwargs):
        data = request.data
        if int(data.get('start_bit')) > 30:
            return Response({'error': 'start_bit must be less than 30'})
        if int(data.get('end_bit')) > 31:
            return Response({'error': 'end_bit must be less than 31'})
        if int(data.get('end_bit')) < int(data.get('start_bit')):
            return Response({'error': 'end_bit must be greater than start_bit'})
        if data.get('RW') not in ["R", "r", "W", "w", "r/w", "R/W"]:
            return Response({'error': 'RW must be R or RW or W'})
        return super().create(request, *args, **kwargs)


class ValueView(ModelViewSet):
    """Value视图"""
    queryset = ValueInfo.objects.all()
    serializer_class = ValueSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('single_reg_uuid', 'id')  # 指定可搜索的字段
    filterset_fields = ('single_reg_uuid', 'id')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('value_uuid'))
        queryset = ValueInfo.objects.filter(value_uuid=request.GET.get('value_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = ValueInfo.objects.get(value_uuid=request.GET.get('value_uuid'))
        # print(request.GET.get('value_uuid'))
        serializer = ValueSerializers(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
