#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import login_view, register_user

urlpatterns = [
    path('login/', login_view, name="login"),
    path('cadastro/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]
