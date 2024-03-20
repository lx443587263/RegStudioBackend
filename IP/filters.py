# filters.py
import django_filters
from django_filters import rest_framework as filters

from IP.models import RegGatherInfo,IpInfo


class IpInfoFilter(filters.FilterSet):
    project = django_filters.CharFilter(field_name='project', lookup_expr="icontains")
    ip_uuid = django_filters.CharFilter(field_name='ip_uuid')
    category = django_filters.CharFilter(field_name='category')
    version = django_filters.CharFilter(field_name='version')
    child_version = django_filters.CharFilter(field_name='child_version')
    ip_name = django_filters.CharFilter(field_name='ip_name')
    private_project = django_filters.BooleanFilter(field_name='private_project')

    class Meta:
        mode = IpInfo
        fields = ['project','ip_uuid','category','version','child_version','ip_name','private_project']

class RegGatherFilter(filters.FilterSet):
    class Meta:
        model = RegGatherInfo  # 模型名
        fields = ['ip_uuid', 'tag', 'reg_gather_name']
