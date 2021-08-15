#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.test import TestCase

from api.serializers import CulturaSerializer, ComunicadoFullSerializer, ComunicadoSerializer
from proagro import util_proagro
from proagro.models import Cultura


class SerializerTest(TestCase):
    """ Test employee serializer """

    def setUp(self):
        self.cultura, _ = Cultura.objects.get_or_create(nome="Cultura 01")
        self.cultura_data = {'id': 1, 'nome': 'cultura01'}
        self.comunicado_data = {'id': 1, 'cpf': util_proagro.gerarCPF(), 'nome': 'Julio',
                                'email': 'julioriffel@gmail.com',
                                'latitude': util_proagro.gerarLatitude(), 'longitude': util_proagro.gerarLongitude(),
                                'cultura': self.cultura, 'datacolheita': util_proagro.gerarDataStr(), 'evento': "GEA"}

    def test_cultura_serializer(self):
        serializer = CulturaSerializer(self.cultura_data)
        self.assertCountEqual(serializer.data.keys(), ['id', 'nome'])

    def test_comunicado_serializer(self):
        serializer = ComunicadoSerializer(self.comunicado_data)
        self.assertCountEqual(serializer.data.keys(),
                              ['id', 'cpf', 'nome', 'cultura', 'latitude', 'longitude', 'datacolheita', 'email',
                               'evento', 'distance'])

    def test_comunicadofull_serializer(self):
        serializer = ComunicadoFullSerializer(self.comunicado_data)
        self.assertCountEqual(serializer.data.keys(),
                              ['id', 'cpf', 'nome', 'cultura', 'latitude', 'longitude', 'datacolheita', 'email',
                               'evento'])
