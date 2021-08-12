#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from django.urls import path

from proagro import views

app_name = 'proagro'
urlpatterns = [
    path("comunicados/novo", views.ComunicadoCreate.as_view(), name='create'),
    path('comunicados/<int:pk>', views.ComunicadoDetail.as_view(), name='detail'),

    path('comunicados/<int:pk>/editar', views.ComunicadoUpdate.as_view(), name='update'),
    path('comunicados/<int:pk>/deletar', views.delete, name='delete'),
    path('', views.ProagroIndex.as_view(), name='index'),

]
