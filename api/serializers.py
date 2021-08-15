#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from rest_framework import serializers

from proagro.models import Cultura, Comunicado


class CulturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultura
        fields = ["id", "nome"]


class ComunicadoSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField('get_distance', read_only=True)

    def get_distance(self, foo):
        try:
            return round(foo.distance.km, 2)
        except:
            return None

    class Meta:
        model = Comunicado
        fields = ["id", "cpf", "nome", "cultura", "latitude", "longitude", "datacolheita", "evento", "email",
                  "distance"]


class ComunicadoFullSerializer(serializers.ModelSerializer):
    divergentes = ComunicadoSerializer(many=True, read_only=True)

    def create(self, validated_data):
        comunicado = Comunicado(**validated_data)
        comunicado.save()
        return comunicado

    class Meta:
        model = Comunicado
        fields = ["id", "cpf", "nome", "cultura", "latitude", "longitude", "datacolheita", "evento", "email",
                  "divergentes"]
