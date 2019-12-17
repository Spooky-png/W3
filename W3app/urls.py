from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.home),
    path(r'dashboard', views.dashboard),
    path(r'login', views.login),
    path(r'logout', views.logout),
    path(r'register', views.register),
    path(r'editprofile', views.editprofile),
    path(r'fight', views.fight),
    path(r'addfighter', views.addfighter),
    path(r'vote/<int:fighter_id>', views.vote),
]