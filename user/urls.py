from django.conf.urls import url
from django.urls import path

from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),
    path('signin/', UserLoginView.as_view()),
]