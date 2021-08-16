#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from django.test import TestCase

from proagro.models import Cultura, Comunicado
from proagro.util_proagro import gerarLatitude, gerarLongitude, gerarCPF


class CulturaClass(TestCase):

    def setUp(cls):
        culturas = ["Arroz", "Feijão", "Milho", "Soja", "Trigo"]
        for cultura in culturas:
            Cultura.objects.create(nome=cultura)

    def test_nome_label(self):
        cultura = Cultura.objects.get(nome="Arroz")
        field_label = cultura._meta.get_field('nome').verbose_name
        self.assertEqual(field_label, 'Nome cultura')

    def test_nome_max_length(self):
        # cultura, c = Cultura.objects.get_or_create(nome="test_nome_max_length")
        cultura = Cultura.objects.get(nome="Arroz")
        max_length = cultura._meta.get_field('nome').max_length
        self.assertEqual(max_length, 100)

    def test_object_str(self):
        # cultura, c = Cultura.objects.get_or_create(nome="test_object_str")
        cultura = Cultura.objects.get(nome="Arroz")
        expected_object_nome = f'{cultura.nome}'
        self.assertEquals(expected_object_nome, str(cultura))

    def test_nome_unique(self):
        Cultura.objects.create(nome="unique")
        with self.assertRaisesRegex(Exception, "already exists"):
            Cultura.objects.create(nome="unique")


class ComunicadoClass(TestCase):

    def setUp(self):
        self.milho, create = Cultura.objects.get_or_create(nome="Milho")
        self.evento = Comunicado.EVENTO_CHOISE[0][0]

        Comunicado.objects.create(cpf=gerarCPF(), nome="Julio Cezar Riffel", latitude=gerarLatitude(),
                                  longitude=gerarLongitude(), cultura=self.milho, evento=self.evento,
                                  datacolheita='2021-07-20')

    def test_get_absolute_url(self):
        comunicado = Comunicado.objects.first()
        self.assertEquals(comunicado.get_absolute_url(), f'/comunicados/{comunicado.id}')

    def test_latitude_longitude_ok(self):
        c = Comunicado(cpf=gerarCPF(), nome="Julio Cezar Riffel", latitude=gerarLatitude(),
                       longitude=gerarLongitude(), cultura=self.milho, evento=self.evento,
                       datacolheita='2021-07-20')
        self.assertEquals(c.clean(), None)

    def test_latitude_min_fail(self):
        c = Comunicado(latitude=-34.01)
        with self.assertRaisesMessage(Exception, "['Latitude no Brasil deve estar entre -34 e +6']"):
            c.clean()

    def test_latitude_max_fail(self):
        c = Comunicado(latitude=6.01)
        with self.assertRaisesMessage(Exception, "['Latitude no Brasil deve estar entre -34 e +6']"):
            c.clean()

    def test_longitude_min_fail(self):
        c = Comunicado(longitude=-74.01)
        with self.assertRaisesMessage(Exception, "['Longitude no Brasil deve estar entre -74 e -34']"):
            c.clean()

    def test_longitude_max_fail(self):
        c = Comunicado(longitude=-6.99)
        with self.assertRaisesMessage(Exception, "['Longitude no Brasil deve estar entre -74 e -34']"):
            c.clean()
