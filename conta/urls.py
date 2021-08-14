#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.urls import path

from conta.views import register_user

urlpatterns = [
    path('cadastro/', register_user, name="register"),

]
