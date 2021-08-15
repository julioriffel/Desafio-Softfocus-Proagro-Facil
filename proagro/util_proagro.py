#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
import datetime
from random import randint


def gerarCPF():
    cpf = [randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return ''.join(map(str, cpf))


def gerarLatitude():
    return randint(-3400, 600) / 100


def gerarLongitude():
    return randint(-7400, -700) / 100


def gerarData():
    return datetime.date.fromtimestamp(randint(1609462861, 1640998861))


def gerarDataStr():
    return datetime.date.fromtimestamp(randint(1609462861, 1640998861)).strftime("%Y-%m-%d")
