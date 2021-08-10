#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from django.conf import settings
from django.db import models


class Comunicado(models.Model):
    EVENTO_CHOISE = [
        (1, ''),
    ]
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    datacolheita = models.DateField()
    evento = models.IntegerField(choices=EVENTO_CHOISE)

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
