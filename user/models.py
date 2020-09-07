from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users Must Have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password) ## hash 해서 저장
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) ## uuid는 범용 고유 식별자, uuid4는 version4
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] ## USERNAME_FIELD와 password는 이미 required라서 넣을 필요 없음

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "login"

class UserProfile(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "profile"