from rest_framework import serializers
from PatternInfo.models import PatternInfo


# Pattern信息序列化
class PatternInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = PatternInfo
        fields = "__all__"
