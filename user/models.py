from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid

from django.utils import timezone
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError("Users Must Have an email address")

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )
        user.set_password(password) ## hash 해서 저장
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, nickname, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) ## uuid는 범용 고유 식별자, uuid4는 version4
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nickname = models.CharField(
        max_length=50,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname',] ## USERNAME_FIELD와 password는 이미 required라서 넣을 필요 없음

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "login"
