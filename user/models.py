from django.db import models

# Create your models here.

class User(models.Model):
    objects = models.Manager()
    name        = models.CharField(max_length=50)
    birthday    = models.DateField(max_length=30)
    password    = models.CharField(max_length=100)
    email       = models.EmailField(max_length=200)
    is_active   = models.BooleanField(default=False)
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)

    class Meta:
        db_table = "users"