#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from proagro.models import Cultura


class CreateCulturaTest(APITestCase):
    def setUp(self):
        self.url = reverse('cultura-list')
        self.client = APIClient()

        self.valid_data = {
            'nome': 'Cultura 01'
        }
        self.invalid_data = {
            'nome': None
        }

    def test_get_list_pass(self):
        request = self.client.get(self.url)
        self.assertEquals(request.status_code, status.HTTP_200_OK)

    def test_create_pass(self):
        response = self.client.post(self.url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEquals(self.valid_data.get("nome"), data.get("nome"))

    def test_create_duplicated_fail(self):
        self.client.post(self.url, data=json.dumps(self.valid_data), content_type='application/json')
        response = self.client.post(self.url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail(self):
        response = self.client.post(self.url, data=json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateCulturaTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.cultura01, _ = Cultura.objects.get_or_create(nome="Cultura 01")
        self.cultura02, _ = Cultura.objects.get_or_create(nome="Cultura 02")

        self.valid_data01 = {'nome': 'Cultura 01 Update'}
        self.invalid_data01 = {'nome': None}

    def test_update_pass(self):
        url = reverse('cultura-detail', kwargs={'pk': self.cultura01.pk})
        response = self.client.put(url, data=json.dumps(self.valid_data01), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_duplicate_fail(self):
        url = reverse('cultura-detail', kwargs={'pk': self.cultura01.pk})
        self.client.put(url, data=json.dumps(self.valid_data01), content_type='application/json')
        url = reverse('cultura-detail', kwargs={'pk': self.cultura02.pk})
        response = self.client.put(url, data=json.dumps(self.valid_data01), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_fail(self):
        url = reverse('cultura-detail', kwargs={'pk': self.cultura01.pk})
        response = self.client.put(url, data=json.dumps(self.invalid_data01), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CulturaDelete(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.cultura = Cultura.objects.create(nome='cultura delete')

    def test_delete_pass(self):
        url = reverse('cultura-detail', kwargs={'pk': self.cultura.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_fail(self):
        url = reverse('cultura-detail', kwargs={'pk': 9999999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
