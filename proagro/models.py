#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


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
            MaxValueValidator(-34),
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

    def clean(self):
        if (self.latitude and not (self.latitude >= -34 and self.latitude <= 6)):
            raise ValidationError(_('Latitude no Brasil deve estar entre -34 e +6'))
        if self.longitude and not (self.longitude >= -74 and self.longitude <= -34):
            raise ValidationError(_('Longitude no Brasil deve estar entre -74 e -34'))

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('proagro:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.ponto = Point(self.latitude, self.longitude)
        super(Comunicado, self).save(*args, **kwargs)

    def divergente(self) -> bool:
        distance = 10000
        qtd = Comunicado.objects.exclude(id=self.pk).exclude(evento=self.evento).filter(
            ponto__distance_lte=(self.ponto, D(m=distance))).filter(
            datacolheita=self.datacolheita).count()
        if qtd > 0:
            return True
        else:
            return False

    @cached_property
    def divergentes(self):
        distance = 10000
        return Comunicado.objects.exclude(id=self.pk).exclude(evento=self.evento).filter(
            datacolheita=self.datacolheita).filter(
            ponto__distance_lte=(self.ponto, D(m=distance))).annotate(
            distance=Distance('ponto', self.ponto)).order_by('distance').select_related('cultura')[:10]

    @cached_property
    def proximo(self, qtd=10):
        return Comunicado.objects.exclude(id=self.pk).annotate(
            distance=Distance('ponto', self.ponto)).order_by('distance').select_related('cultura')[:qtd]
