#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Cultura(models.Model):
    nome = models.CharField("Nome cultura", max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Comunicado(models.Model):
    EVENTO_CHOISE = [
        ('CHV', 'Chuva Excessica'),
        ('GEA', 'Geada'),
        ('GRA', 'Granizo'),
        ('SEC', 'Seca'),
        ('VEN', 'Vendaval'),
        ('RAI', 'Raio')

    ]
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    latitude = models.FloatField(
        validators=[
            MaxValueValidator(6),
            MinValueValidator(-34)
        ]
    )
    longitude = models.FloatField(
        validators=[
            MaxValueValidator(-7),
            MinValueValidator(-74)
        ]
    )
    ponto = PointField(blank=True, null=True)
    cultura = models.ForeignKey(Cultura, on_delete=models.RESTRICT)
    evento = models.CharField(max_length=3, choices=EVENTO_CHOISE)
    datacolheita = models.DateField()

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('proagro:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.ponto = Point(self.latitude, self.longitude)
        super(Comunicado, self).save(*args, **kwargs)
