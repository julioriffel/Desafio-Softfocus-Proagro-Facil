#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
import datetime
from random import randint


def gerarCPF():
    cpf = ''
    for i in range(11):
        cpf += str(randint(0, 9))
    return cpf


def gerarLatitude():
    return randint(-3400, 600) / 100


def gerarLongitude():
    return randint(-7400, -700) / 100


def gerarData():
    return datetime.date.fromtimestamp(randint(1609462861, 1640998861))


def gerarDataStr():
    return datetime.date.fromtimestamp(randint(1609462861, 1640998861)).strftime("%Y-%m-%d")
