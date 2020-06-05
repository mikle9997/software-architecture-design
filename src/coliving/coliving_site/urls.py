from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
  path('search', views.search),
  path('rent', views.rent),
  path('announcemet', views.announcemet),
  path('account', views.account),
  path('login', views.login),
  path('register', views.register),
  path('logout', views.logout),
  path('changeinfo', views.changeInfo),
  path('', views.index),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
