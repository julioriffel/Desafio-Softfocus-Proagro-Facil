#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class RegisterViewTest(TestCase):

    def setUp(self):
        self.register_valid = {'username': 'register_user', 'email': 'register_user@mailinator.com',
                               'password1': 'dsb76AS(Bh##', 'password2': 'dsb76AS(Bh##'}
        self.register_invalid_pass = {'username': 'register_user', 'email': 'register_user@mailinator.com',
                                      'password1': '8@password1', 'password2': 'password2'}

        self.register_invalid_parameter = {'username': 'register_user', 'email': 'register_user@mailinator.com',
                                           'password1': '8@password1'}

    def test_view_register_pass(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_register_post_pass(self):
        response = self.client.post(reverse('register'), self.register_valid)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    def test_view_register_post_parameter_fail(self):
        response = self.client.post(reverse('register'), self.register_invalid_parameter)
        msg = response.context['msg']
        self.assertEqual(msg, f'Form is not valid')
        success = response.context['success']
        self.assertNotEqual(success, True)

    def test_view_register_post_pass_fail(self):
        response = self.client.post(reverse('register'), self.register_invalid_pass)
        msg = response.context['msg']
        self.assertEqual(msg, f'Form is not valid')
        success = response.context['success']
        self.assertNotEqual(success, True)
