#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from django.urls import path

from proagro import views

app_name = 'proagro'
urlpatterns = [
    path('', views.ProagroIndex.as_view(), name='index'),
]
