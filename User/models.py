import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        username = username
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        # user.save(using=self.queryset.db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


# Create your models here.
class UserInfo(AbstractBaseUser, PermissionsMixin):
    """用户Info"""
    user_uuid = models.CharField(verbose_name="UserUuid", max_length=128, null=False, unique=True)
    username = models.CharField(verbose_name="Name", max_length=64, unique=True)
    password = models.CharField(verbose_name="Password", max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    position = models.CharField(verbose_name="position", max_length=64)
    create_date = models.DateField(verbose_name="CreateDate")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if sender.name == 'User':
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username="admin", password="123456", user_uuid=str(uuid.uuid4()),
                                          create_date=datetime.now().strftime('%Y-%m-%d'), position="admin")
