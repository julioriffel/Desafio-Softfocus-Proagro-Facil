#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.test import TestCase

from proagro.models import Cultura, Comunicado


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
    @classmethod
    def setUpTestData(cls):
        milho, create = Cultura.objects.get_or_create(nome="Milho")
        evento = Comunicado.EVENTO_CHOISE[0][0]

        Comunicado.objects.create(cpf="06889117905", nome="Julio Cezar Riffel", latitude=-23.123, longitude=-52.123,
                                  cultura=milho, evento=evento, datacolheita='2021-07-20')

    def test_get_absolute_url(self):
        comunicado = Comunicado.objects.get(id=1)
        self.assertEquals(comunicado.get_absolute_url(), f'/comunicados/{comunicado.id}')
