from rest_framework import serializers
from User.models import UserInfo


# IP序列化器
class UserInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"