from django.urls import path
from . import views

urlpatterns = [
  path('search', views.search),
  path('rent', views.rent),
  path('', views.index),
]