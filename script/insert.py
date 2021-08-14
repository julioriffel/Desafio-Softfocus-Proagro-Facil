#  Copyright (c) 2021-2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
import datetime
import os
from random import randint

import django

from proagro import util_proagro

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from proagro.models import Cultura, Comunicado

ids_cultura = []
culturas = ["Arroz", "Feijão", "Milho", "Soja", "Trigo"]
for cultura in culturas:
    item, c = Cultura.objects.get_or_create(nome=cultura)
    ids_cultura.append(item.id)

for id in range(25):
    cultura_id = ids_cultura[randint(0, len(ids_cultura) - 1)]

    Comunicado.objects.create(nome=f"Nome {id}",
                              cultura_id=cultura_id,
                              cpf=util_proagro.gerarCPF(),
                              email=f"nome{id}@mail.com",
                              latitude=util_proagro.gerarLatitude(),
                              longitude=util_proagro.gerarLongitude(),
                              datacolheita=datetime.date.fromtimestamp(randint(1609462861, 1640998861)),
                              evento=Comunicado.EVENTO_CHOISE[randint(0, len(Comunicado.EVENTO_CHOISE) - 1)][0])
