from rest_framework import serializers
from IP.models import IpInfo, RegGatherInfo, SingleRegInfo, ValueInfo


# IP序列化器
class IpSerializers(serializers.ModelSerializer):
    class Meta:
        model = IpInfo
        fields = "__all__"


# RegGather序列化器
class RegGatherSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegGatherInfo
        fields = "__all__"


# SingleReg序列化器
class SingleRegSerializers(serializers.ModelSerializer):
    class Meta:
        model = SingleRegInfo
        fields = "__all__"


# Value序列化器
class ValueSerializers(serializers.ModelSerializer):
    class Meta:
        model = ValueInfo
        fields = "__all__"
