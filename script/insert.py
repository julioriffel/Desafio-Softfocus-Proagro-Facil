#  Copyright (c) 2021-2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
import datetime
import os
from random import randint

import django
from django.contrib.gis.geos import Point

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from proagro.models import Cultura, Comunicado


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

for id in range(25):
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
