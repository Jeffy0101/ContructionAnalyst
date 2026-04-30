from django.urls import path
from . import auth_views, views

urlpatterns = [
    path('auth/register', auth_views.register),
    path('auth/login', auth_views.login),
    path('auth/me', auth_views.me),
    path('analyser', views.analyser),
    path('historique', views.historique),
    path('dataset', views.dataset),
    path('features', views.features),
]
