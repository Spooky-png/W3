from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'', views.home),
    path(r'dashboard', views.dashboard),
    path(r'login', views.login),
    path(r'logout', views.logout),
    path(r'register', views.register),
    path(r'editprofile', views.editprofile),
    path(r'fight', views.fight),
    path(r'addfighter', views.addfighter),
    path(r'viewprofile/<int:user_id>', views.viewprofile),
    path(r'vote/<int:fighter_id>', views.vote),
    path(r'upload', views.upload),
    path(r'portfolio', views.portfolio)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)