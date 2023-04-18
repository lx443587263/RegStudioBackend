from django.db import models


# Create your models here.
class IpInfo(models.Model):
    """Ip信息表"""
    ip_uuid = models.CharField(verbose_name="IpUuid", unique=True, max_length=128, null=False)
    ip_name = models.CharField(verbose_name="IpName", max_length=64)
    private_project = models.BooleanField(verbose_name="PrivateProject")
    description = models.TextField(verbose_name="IpDescription")
    start_date = models.DateField(verbose_name="StartDate")
    status = models.CharField(verbose_name="Status", max_length=32)
    end_date = models.DateField(verbose_name="EndDate")
    create_user = models.CharField(verbose_name="CreateUser", max_length=64, null=False)
    version = models.CharField(verbose_name="Version", max_length=64, null=False,default="v1.0")


class RegGatherInfo(models.Model):
    """RegGather信息表"""
    # ip_uuid = models.CharField(verbose_name="IpUuid", max_length=128, null=False)
    ip_uuid = models.ForeignKey(IpInfo, on_delete=models.CASCADE, to_field='ip_uuid', db_column="ip_uuid",
                                max_length=128, null=False)
    reg_gather_uuid = models.CharField(verbose_name="RegGatherUuid", max_length=128, null=False, unique=True)
    tag = models.CharField(verbose_name="Tag", max_length=64)
    offset = models.CharField(verbose_name="Offset", max_length=64, unique=True)
    reg_gather_name = models.CharField(verbose_name="RegGatherName", max_length=128)
    description = models.TextField(verbose_name="Description")
    reset = models.CharField(verbose_name="Reset", max_length=64)

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
    RW = models.CharField(verbose_name="R/W", max_length=16)
    field = models.CharField(verbose_name="Field", max_length=128)
    note = models.CharField(verbose_name="Note", max_length=128, null=True, blank=True)
    description = models.TextField(verbose_name="Description")


class ValueInfo(models.Model):
    """单个Reg值的Info表"""
    # single_reg_uuid = models.CharField(verbose_name="ValueId", max_length=64, null=False)
    single_reg_uuid = models.ForeignKey(SingleRegInfo, to_field='single_reg_uuid', on_delete=models.CASCADE,
                                        db_column="single_reg_uuid")
    value_uuid = models.CharField(verbose_name="value_uuid", max_length=128, null=False, unique=True)
    valueId = models.CharField(verbose_name="ValueId", max_length=64)
    value = models.IntegerField(verbose_name="Value")
    description = models.TextField(verbose_name="Description")
