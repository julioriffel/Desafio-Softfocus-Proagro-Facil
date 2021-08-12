#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
import datetime

from django.test import TestCase

from proagro.forms import ComunicadoForm
from proagro.models import Cultura


class ComunicadoFormTest(TestCase):
    data_valido = None

    def setUp(cls):
        culturas = ["Arroz", "Feijão", "Milho", "Soja", "Trigo"]
        for cultura in culturas:
            Cultura.objects.create(nome=cultura)

        milho = Cultura.objects.get(nome="Milho")
        cls.data_valido = {'cpf': '06889117905', 'nome': 'Julio', 'email': 'julioriffel@gmail.com',
                           'latitude': -22.123, 'longitude': -52.123, 'cultura': milho.id,
                           'datacolheita': datetime.date.today(), 'evento': "GEA"}

    def test_firm_valid(self):
        form = ComunicadoForm(data=self.data_valido)
        self.assertTrue(form.is_valid())

    def test_latitude_max_failure(self):
        lat_data = self.data_valido
        lat_data['latitude'] = 7
        form = ComunicadoForm(data=lat_data)
        self.assertFalse(form.is_valid())

    def test_latitude_max_pass(self):
        lat_data = self.data_valido
        lat_data['latitude'] = 6
        form = ComunicadoForm(data=lat_data)
        self.assertTrue(form.is_valid())

    def test_latitude_min_failure(self):
        lat_data = self.data_valido
        lat_data['latitude'] = -35
        form = ComunicadoForm(data=lat_data)
        self.assertFalse(form.is_valid())

    def test_latitude_min_pass(self):
        lat_data = self.data_valido
        lat_data['latitude'] = -34
        form = ComunicadoForm(data=lat_data)
        self.assertTrue(form.is_valid())

    def test_longitude_max_failure(self):
        lat_data = self.data_valido
        lat_data['longitude'] = -6
        form = ComunicadoForm(data=lat_data)
        self.assertFalse(form.is_valid())

    def test_longitude_max_pass(self):
        lat_data = self.data_valido
        lat_data['longitude'] = -7
        form = ComunicadoForm(data=lat_data)
        self.assertTrue(form.is_valid())

    def test_longitude_min_failure(self):
        lat_data = self.data_valido
        lat_data['longitude'] = -75
        form = ComunicadoForm(data=lat_data)
        self.assertFalse(form.is_valid())

    def test_longitude_min_pass(self):
        lat_data = self.data_valido
        lat_data['longitude'] = -74
        form = ComunicadoForm(data=lat_data)
        self.assertTrue(form.is_valid())

    def test_email_failure(self):
        current_data = self.data_valido
        current_data['email'] = "@gmail.com"
        form = ComunicadoForm(data=current_data)
        self.assertFalse(form.is_valid())

    def test_cultura_label(self):
        form = ComunicadoForm()
        self.assertTrue(
            form.fields['cultura'].label == None or form.fields['cultura'].label == 'Cultura')

    def test_cultura_help_text(self):
        form = ComunicadoForm()
        self.assertEqual(form.fields['cultura'].help_text, 'Selecione a cultura')
