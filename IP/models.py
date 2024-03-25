from django.db import models
from User.models import UserInfo


# Create your models here.
class IpInfo(models.Model):
    """Ip信息表"""
    ip_uuid = models.CharField(verbose_name="IpUuid", unique=True, max_length=128, null=False)
    ip_name = models.CharField(verbose_name="IpName", max_length=64)
    private_project = models.BooleanField(verbose_name="PrivateProject")
    description = models.TextField(verbose_name="IpDescription", null=True)
    start_date = models.DateField(verbose_name="StartDate", null=True)
    status = models.CharField(verbose_name="Status", max_length=32)
    end_date = models.DateField(verbose_name="EndDate", null=True)
    create_user = models.CharField(verbose_name="CreateUser", max_length=64, null=False)
    version = models.CharField(verbose_name="Version", max_length=64, null=False, default="v1.0")
    category = models.CharField(verbose_name="Category", max_length=128, null=False)
    project = models.CharField(verbose_name="Project", max_length=1024, null=True)
    tags = models.CharField(verbose_name="Tags", max_length=256, null=True)
    child_version = models.CharField(verbose_name="Child Version", max_length=256, null=True)
    permission = models.CharField(verbose_name="Permission List", max_length=256, null=True)
    see_permission = models.CharField(verbose_name="see_permission", max_length=256, null=True)
    reg_version = models.CharField(verbose_name="Reg Version", max_length=64, null=True)

class RegGatherInfo(models.Model):
    """RegGather信息表"""
    # ip_uuid = models.CharField(verbose_name="IpUuid", max_length=128, null=False)
    ip_uuid = models.ForeignKey(IpInfo, on_delete=models.CASCADE, to_field='ip_uuid', db_column="ip_uuid",
                                max_length=128, null=False)
    reg_gather_uuid = models.CharField(verbose_name="RegGatherUuid", max_length=128, null=False, unique=True)
    tag = models.CharField(verbose_name="Tag", max_length=64)
    offset = models.CharField(verbose_name="Offset", max_length=64)
    reg_gather_name = models.CharField(verbose_name="RegGatherName", max_length=128)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    reset = models.CharField(verbose_name="Reset", max_length=64, null=True)
    address = models.CharField(verbose_name="Address", max_length=64, null=True)
    retention = models.CharField(verbose_name="Retention", max_length=64, null=True, blank=True)
    reg_ram = models.CharField(verbose_name="reg/ram", max_length=64, null=True)

    class Meta:
        db_table = 'IP_reggatherinfo'
        verbose_name = "RegGather信息"


class SingleRegInfo(models.Model):
    """单个最小RegInfo表"""
    # reg_gather_uuid = models.CharField(verbose_name="RegGatherUuid", max_length=128, null=False)
    reg_gather_uuid = models.ForeignKey(RegGatherInfo, to_field='reg_gather_uuid', on_delete=models.CASCADE,
                                        db_column="reg_gather_uuid")
    single_reg_uuid = models.CharField(verbose_name="SingleRegUuid", max_length=128, null=False, unique=True)
    start_bit = models.CharField(verbose_name="StartBit", max_length=16)
    end_bit = models.CharField(verbose_name="EndBit", max_length=16)
    reset_value = models.CharField(verbose_name="ResetValue", max_length=64)
    RW = models.CharField(verbose_name="R/W", max_length=16)
    field = models.CharField(verbose_name="Field", max_length=128)
    note = models.CharField(verbose_name="Note", max_length=128, null=True, blank=True)
    description = models.TextField(verbose_name="Description", null=True)
    hw_RW = models.CharField(verbose_name="HW R/W", max_length=16, null=True)


class ValueInfo(models.Model):
    """单个Reg值的Info表"""
    # single_reg_uuid = models.CharField(verbose_name="ValueId", max_length=64, null=False)
    single_reg_uuid = models.ForeignKey(SingleRegInfo, to_field='single_reg_uuid', on_delete=models.CASCADE,
                                        db_column="single_reg_uuid")
    value_uuid = models.CharField(verbose_name="value_uuid", max_length=128, null=False, unique=True)
    valueId = models.CharField(verbose_name="ValueId", max_length=64, null=True)
    value = models.CharField(verbose_name="Value", max_length=64)
    description = models.TextField(verbose_name="Description", null=True)


class FilesModel(models.Model):
    file = models.FileField(upload_to='uploads/')

    class Meta:
        db_table = 'files_storage'
        ordering = ['-id']


class TemplateFilesModel(models.Model):
    file = models.FileField(upload_to='template/')
    name = models.CharField(verbose_name="FileName", max_length=128)
    size = models.CharField(verbose_name="Size", max_length=128)
    file_uuid = models.CharField(verbose_name="file_uuid", max_length=128, null=False, unique=True)

    class Meta:
        db_table = 'template_files_storage'
        ordering = ['-id']


class CategoryInfo(models.Model):
    category = models.CharField(verbose_name="Category", max_length=128, unique=True, null=False)

class ProjectInfo(models.Model):
    project_uuid = models.CharField(verbose_name="ProjectUuid", unique=True, max_length=128, null=False)
    project = models.CharField(verbose_name="ProjectName", max_length=128, unique=False, null=True)
    version = models.CharField(verbose_name="Version", max_length=128,null=False)
    has_ip = models.CharField(verbose_name="HasIP",max_length=1024,null=True)

class ProjectChange(models.Model):
    operate_ip_name = models.CharField(verbose_name="OpIpName",max_length=128,null=True)
    source_project = models.CharField(verbose_name="SourceProject", max_length=128,null=True)
    source_project_uuid = models.CharField(verbose_name="SourceProjectUuid", max_length=128, null=True)
    des_project = models.CharField(verbose_name="DesProject", max_length=128,null=True)
    des_project_uuid = models.CharField(verbose_name="SourceProjectUuid", max_length=128,null=True)
    edit_user = models.CharField(verbose_name="EditUser", max_length=128,null=False)
    data = models.DateTimeField(verbose_name="StartDate", null=True)
class OpLogs(models.Model):
    """操作日志表"""
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'op_logs'


class AccessTimeOutLogs(models.Model):
    """超时操作日志表"""
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'access_timeout_logs'


class modificationInfo(models.Model):
    user = models.CharField(verbose_name="user", max_length=128)
    user_uuid = models.ForeignKey(UserInfo, to_field='user_uuid', on_delete=models.CASCADE,
                                  db_column="user_uuid")
    data = models.DateTimeField(verbose_name="StartDate")
    former_content = models.TextField(null=True, verbose_name='Former Data')
    modify_content = models.TextField(null=True, verbose_name='Modify Data')
    modify_model = models.CharField(verbose_name="Modify Model", max_length=64)

    class Meta:
        db_table = 'modificationInfo'


class IpPageFilesModel(models.Model):
    file = models.FileField(upload_to='IpPage/')
    name = models.CharField(verbose_name="FileName", max_length=128)
    version = models.CharField(verbose_name="Version", max_length=128)
    commit_content = models.CharField(verbose_name="Commit Content", max_length=256)
    create_user = models.CharField(verbose_name="Create User", max_length=128)
    upload_data = models.CharField(verbose_name="Upload_data",max_length=128)
    file_uuid = models.CharField(verbose_name="file_uuid", max_length=128, null=False, unique=True)
    ip_uuid = models.ForeignKey(IpInfo, on_delete=models.CASCADE, to_field='ip_uuid', db_column="ip_uuid",
                                max_length=128, null=False)

    class Meta:
        db_table = 'ip_page_files_storage'
        ordering = ['-id']
