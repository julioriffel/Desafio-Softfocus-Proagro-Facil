#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
import datetime
from random import randint

from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse

from proagro.models import Cultura, Comunicado


class ComunicadoViewTest(TestCase):
    exemplo_valido = None

    def setUp(cls):

        user = User.objects.create_user(username='user1', password='abcd1234')
        user.save()

        def gerarCPF():
            cpf = ''
            for i in range(11):
                cpf += str(randint(0, 9))
            return cpf

        ids_cultura = []
        culturas = ["Arroz", "Feijão", "Milho", "Soja", "Trigo"]
        for cultura in culturas:
            item, c = Cultura.objects.get_or_create(nome=cultura)
            ids_cultura.append(item.id)

        milho = Cultura.objects.get(nome="Milho")
        cls.exemplo_valido = {'cpf': '06889117905', 'nome': 'Julio', 'email': 'julioriffel@gmail.com',
                              'latitude': -22.123, 'longitude': -52.123, 'cultura': milho.id,
                              'datacolheita': datetime.date.today(), 'evento': "GEA"}

        for id in range(17):
            cultura_id = ids_cultura[randint(0, len(ids_cultura) - 1)]
            latitude = randint(-3400, 600) / 100
            longitude = randint(-7400, -700) / 100
            ponto = Point(latitude, longitude)
            Comunicado.objects.create(nome=f"Nome {id}",
                                      cultura_id=cultura_id,
                                      cpf=gerarCPF(),
                                      email=f"nome{id}@mail.com",
                                      latitude=latitude,
                                      longitude=longitude,
                                      ponto=ponto,
                                      datacolheita=datetime.date.fromtimestamp(randint(1609462861, 1640998861)),
                                      evento=Comunicado.EVENTO_CHOISE[randint(0, len(Comunicado.EVENTO_CHOISE) - 1)][0])

    def test_view_home_login_required(self):
        response = self.client.get(reverse('proagro:index'))
        self.assertRedirects(response, '/conta/login/?next=/')

    def test_view_comunicados_create_login_required(self):
        response = self.client.get(reverse('proagro:create'))
        self.assertRedirects(response, '/conta/login/?next=/comunicados/novo')

    def test_view_comunicados_delete_login_required_redirect(self):
        comunicado_1 = Comunicado.objects.first()
        response = self.client.get(reverse('proagro:delete', kwargs={'pk': comunicado_1.id}))
        self.assertRedirects(response, f'/conta/login/?next=/comunicados/{comunicado_1.id}/deletar')

    def test_logged_comunicados_list(self):
        self.client.login(username='user1', password='abcd1234')
        response = self.client.get(reverse('proagro:index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['object_list']) == 7)

    def test_comunicados_orded(self):
        self.client.login(username='user1', password='abcd1234')
        response = self.client.get(reverse('proagro:index'))

        last_data = None
        for comunicado in response.context['object_list']:
            if last_data == None:
                last_data = comunicado.datacolheita
            else:
                self.assertTrue(last_data >= comunicado.datacolheita)
                last_data = comunicado.datacolheita

    def test_comunicado_detail_pass(self):
        self.client.login(username='user1', password='abcd1234')
        comunicado_1 = Comunicado.objects.first()
        response = self.client.get(reverse('proagro:detail', kwargs={'pk': comunicado_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proagro/comunicado_detail.html')

    def test_comunicado_form_update_acess_pass(self):
        self.client.login(username='user1', password='abcd1234')
        comunicado_1 = Comunicado.objects.first()
        response = self.client.get(reverse('proagro:update', kwargs={'pk': comunicado_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proagro/comunicado_form.html')

    def test_comunicado_form_create_post_pass(self):
        self.client.login(username='user1', password='abcd1234')

        response = self.client.post(reverse('proagro:create'), self.exemplo_valido)
        self.assertEqual(response.status_code, 302)

    def test_comunicado_form_update_post_pass(self):
        self.client.login(username='user1', password='abcd1234')
        comunicado_1 = Comunicado.objects.first()

        response = self.client.post(reverse('proagro:update', kwargs={'pk': comunicado_1.id, }),
                                    self.exemplo_valido)
        self.assertRedirects(response, reverse('proagro:detail', kwargs={'pk': comunicado_1.id}))

    def test_view_comunicados_delete_login_required(self):
        self.client.login(username='user1', password='abcd1234')
        comunicado_1 = Comunicado.objects.first()
        response = self.client.get(reverse('proagro:delete', kwargs={'pk': comunicado_1.id}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaisesMessage(Exception, "Comunicado matching query does not exist."):
            Comunicado.objects.get(id=comunicado_1.id)

    def test_comunicado_search(self):
        Comunicado.objects.filter(cpf='11111111111').update(cpf='00000000000')
        Comunicado.objects.filter(cpf='11111111111').update(cpf='00000000000')
        unico = Comunicado.objects.first()
        unico.cpf = '11111111111'
        unico.save()

        self.client.login(username='user1', password='abcd1234')
        response = self.client.get(reverse('proagro:index') + '?pesquisa=11111111111')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)
        self.assertTrue(len(response.context['object_list']) == 1)

    def test_comunicado_detail_divergente_pass(self):

        self.client.login(username='user1', password='abcd1234')

        response = self.client.post(reverse('proagro:create'), self.exemplo_valido)
        self.assertEqual(response.status_code, 302)

        exemplo_dif = self.exemplo_valido
        exemplo_dif['evento'] = 'VEN'
        response = self.client.post(reverse('proagro:create'), exemplo_dif)
        self.assertEqual(response.status_code, 302)

        comunicado_1 = Comunicado.objects.last()
        response = self.client.get(reverse('proagro:detail', kwargs={'pk': comunicado_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proagro/comunicado_detail.html')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 3)
        self.assertEqual(str(messages[0]), 'Salvo')
        self.assertEqual(str(messages[1]), 'Salvo')
        self.assertEqual(str(messages[2]), 'Atenção: Evento Divergente')
