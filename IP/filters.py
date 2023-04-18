# filters.py
from django_filters import rest_framework as filters

from IP.models import RegGatherInfo


class RegGatherFilter(filters.FilterSet):
    class Meta:
        model = RegGatherInfo  # 模型名
        fields = ['ip_uuid', 'tag', 'reg_gather_name']
