from django.conf.urls import url
from django.urls import path

from .views import (
    UserRegistrationView, 
    UserLoginView, 
    UserView,
    UserProfileView,
    PasswordChangeView,
    kakaoCallbackView,
)

urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),
    path('signin/', UserLoginView.as_view()),
    path('', UserView.as_view()),
    path('signin/kakao/call_back/', kakaoCallbackView.as_view()),
    path('<str:id>', UserProfileView.as_view()),
    path('pwc/', PasswordChangeView.as_view()),
]