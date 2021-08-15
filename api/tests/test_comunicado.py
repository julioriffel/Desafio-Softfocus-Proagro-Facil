#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

import json
from random import randint

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from proagro import util_proagro
from proagro.models import Comunicado, Cultura


class CreateComunicadoTest(APITestCase):
    def setUp(self):
        self.url = reverse('comunicado-list')
        self.client = APIClient()

        User.objects.create_user(username='user1', password='abcd1234')
        self.cultura, _ = Cultura.objects.get_or_create(nome="Cultura 001")
        self.valid_data = {'cpf': '06889117905', 'nome': 'Julio', 'email': 'julioriffel@gmail.com',
                           'latitude': -22.123, 'longitude': -52.123, 'cultura': self.cultura.id,
                           'datacolheita': '2021-10-10', 'evento': "GEA"}


        self.invalid_data = {'cpf': '06889117905', 'nome': 'Julio', 'email': 'julioriffel@gmail.com',
                             'latitude': -22.123, 'longitude': None, 'cultura_id': self.cultura.id,
                             'datacolheita': '2021-01-30', 'evento': "GEA"}

    def test_get_list_pass(self):
        request = self.client.get(self.url)
        self.assertEquals(request.status_code, status.HTTP_200_OK)

    def test_create_pass(self):
        response = self.client.post(self.url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEquals(self.valid_data.get("cpf"), data.get("cpf"))
        self.assertEquals(self.valid_data.get("nome"), data.get("nome"))
        self.assertEquals(self.valid_data.get("email"), data.get("email"))
        self.assertEquals(self.valid_data.get("latitude"), data.get("latitude"))
        self.assertEquals(self.valid_data.get("longitude"), data.get("longitude"))
        self.assertEquals(self.valid_data.get("cultura"), data.get("cultura"))
        self.assertEquals(self.valid_data.get("datacolheita"), data.get("datacolheita"))
        self.assertEquals(self.valid_data.get("evento"), data.get("evento"))

    def test_create_obrigatorios_fail(self):
        response = self.client.post(self.url, data=json.dumps(self.valid_data.copy().pop('cpf')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=json.dumps(self.valid_data.copy().pop('nome')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=json.dumps(self.valid_data.copy().pop('latitude')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=json.dumps(self.valid_data.copy().pop('longitude')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=json.dumps(self.valid_data.copy().pop('cultura')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=json.dumps(self.valid_data.copy().pop('evento')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, data=json.dumps(self.valid_data.copy().pop('datacolheita')),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_logged_pass(self):
        self.client.login(username='user1', password='abcd1234')
        response = self.client.post(self.url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_latitude_min_fail(self):
        data = self.valid_data.copy()
        data['latitude'] = -35.11
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_latitude_max_fail(self):
        data = self.valid_data.copy()
        data['latitude'] = 7.11
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_longitude_min_fail(self):
        data = self.valid_data.copy()
        data['longitude'] = -74.01
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_longitude_max_fail(self):
        data = self.valid_data.copy()
        data['longitude'] = -6.99
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateComunicadoTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.cultura, _ = Cultura.objects.get_or_create(nome="Cultura 001")

        self.comunicado01 = Comunicado.objects.create(nome=f"Nome ",
                                                      cultura_id=self.cultura.id,
                                                      cpf=util_proagro.gerarCPF(),
                                                      email=f"nome@mail.com",
                                                      latitude=util_proagro.gerarLatitude(),
                                                      longitude=util_proagro.gerarLongitude(),
                                                      datacolheita=util_proagro.gerarData(),
                                                      evento=Comunicado.EVENTO_CHOISE[
                                                          randint(0, len(Comunicado.EVENTO_CHOISE) - 1)][0])

        self.valid_data = {'cpf': '06889117905', 'nome': 'Julio', 'email': 'julioriffel@gmail.com',
                           'latitude': -22.123, 'longitude': -52.123, 'cultura': self.cultura.id,
                           'datacolheita': '2021-10-10', 'evento': "GEA"}

        self.invalid_data = {'cpf': '06889117905', 'nome': 'Julio', 'email': 'julioriffel@gmail.com',
                             'latitude': -22.123, 'longitude': None, 'cultura_id': self.cultura.id,
                             'datacolheita': '2021-01-30', 'evento': "GEA"}

    def test_update_pass(self):
        url = reverse('comunicado-detail', kwargs={'pk': self.comunicado01.pk})
        response = self.client.put(url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_null_fail(self):
        url = reverse('comunicado-detail', kwargs={'pk': self.comunicado01.pk})
        response = self.client.put(url, data=json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ComunicadoDelete(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.cultura, _ = Cultura.objects.get_or_create(nome="Cultura 001")
        self.comunicado = Comunicado.objects.create(nome=f"Nome ",
                                                    cultura_id=self.cultura.id,
                                                    cpf=util_proagro.gerarCPF(),
                                                    email=f"nome@mail.com",
                                                    latitude=util_proagro.gerarLatitude(),
                                                    longitude=util_proagro.gerarLongitude(),
                                                    datacolheita=util_proagro.gerarData(),
                                                    evento=Comunicado.EVENTO_CHOISE[
                                                        randint(0, len(Comunicado.EVENTO_CHOISE) - 1)][0])

    def test_delete_pass(self):
        url = reverse('comunicado-detail', kwargs={'pk': self.comunicado.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_fail(self):
        url = reverse('comunicado-detail', kwargs={'pk': 9999999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
