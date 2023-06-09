from rest_framework import serializers
from IP.models import IpInfo, RegGatherInfo, SingleRegInfo, ValueInfo, FilesModel, TemplateFilesModel, OpLogs, \
    AccessTimeOutLogs, CategoryInfo, modificationInfo


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


# 种类序列化器
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CategoryInfo
        fields = "__all__"


# 导入文件序列化器
class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesModel
        fields = '__all__'


# 导出文件模版序列化器
class TemplateFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateFilesModel
        fields = '__all__'


# 操作记录序列化器
class OpLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpLogs
        fields = '__all__'


# 超时记录序列化器
class AccessTimeOutLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTimeOutLogs
        fields = '__all__'


# 修改记录序列化器
class modificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = modificationInfo
        fields = '__all__'
