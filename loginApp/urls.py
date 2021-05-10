from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('register', views.register),
    path('user_register', views.validate_register),
    path('user_validate', views.validate_login),
    path('logout', views.logout_view),
    ]