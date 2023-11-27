from django.db import models


# Create your models here.

class PatternInfo(models.Model):
    """pattern信息表"""
    TEST_ITEM = models.CharField(verbose_name="TestItem", max_length=128,null=True)
    PATTERN_NAME = models.CharField(verbose_name="PatternName", max_length=128,null=True)
    TEST_CATEGORY = models.CharField(verbose_name="TestGategory", max_length=128,null=True)
    TEST_PURPOSE = models.CharField(verbose_name="TestPurpose", max_length=128,null=True)
    TEST_PROCESS = models.CharField(verbose_name="TestProcess", max_length=512,null=True)
    TEST_NOTES = models.CharField(verbose_name="TestNotes", max_length=128,null=True)
    USER = models.CharField(verbose_name="User", max_length=64,null=True)
    TIME = models.CharField(verbose_name="Time", max_length=128,null=True)
    RTL_VERSION = models.CharField(verbose_name="Rtl_Version", max_length=128,null=True)
    NETLIST_VERSION = models.CharField(verbose_name="NetlistVersion", max_length=128,null=True)
    SIM_MODE = models.CharField(verbose_name="SimMode", max_length=128,null=True)
    TOOL = models.CharField(verbose_name="Tool", max_length=64,null=True)
    CORNER = models.CharField(verbose_name="Corner", max_length=128,null=True)
    MTM = models.CharField(verbose_name="Mtm", max_length=128,null=True)
    SIM_SEED = models.CharField(verbose_name="SimSeed",max_length=128,null=True)
    TWO_NODE = models.BooleanField(verbose_name="TwoNode",null=True)
    MBIST = models.BooleanField(verbose_name="Mbist",null=True)
    FPGA_FLOW = models.CharField(verbose_name="FpgaFlow", max_length=128,null=True)
    FPGA_WORK = models.CharField(verbose_name="FpgaWork", max_length=128,null=True)
    WORK_PATH = models.CharField(verbose_name="WorkPath", max_length=128,null=True)
    LOG_NAME = models.CharField(verbose_name="LogName", max_length=128,null=True)
    SIM_RESULTS = models.CharField(verbose_name="SimResults", max_length=128,null=True)
    CHECK_WAVE = models.BooleanField(verbose_name="CheckWave",null=True)
    JTAG_ACCESS = models.BooleanField(verbose_name="JtagAccess",null=True)
    PATTERN_MD5 = models.CharField(verbose_name="PatternMd5", max_length=128,null=True)
    PROJECT_NAME = models.CharField(verbose_name="ProjectName", max_length=128,null=True)
