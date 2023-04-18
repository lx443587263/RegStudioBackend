# filters.py
from django_filters import rest_framework as filters

from User.models import UserInfo


class UserFilter(filters.FilterSet):
    class Meta:
        model = UserInfo  # 模型名
        fields = ['user_uuid', 'username', 'password', 'position']
