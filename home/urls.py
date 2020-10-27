from django.conf.urls import url
from django.urls import path, include
from .views import HomeListView

urlpatterns = [
    path('', HomeListView.as_view()),
]