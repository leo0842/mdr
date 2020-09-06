from django.urls import path, include
from .views import UserApi

urlpatterns = [
    path('register/', UserApi.as_view())
]