#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from rest_framework import viewsets

from api.serializers import CulturaSerializer, ComunicadoSerializer
from proagro.models import Cultura, Comunicado


class CulturaViewSet(viewsets.ModelViewSet):
    queryset = Cultura.objects.order_by('id')
    serializer_class = CulturaSerializer


class ComunicadoViewSet(viewsets.ModelViewSet):
    queryset = Comunicado.objects.order_by('-datacolheita')
    serializer_class = ComunicadoSerializer

    def perform_create(self, serializer):
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        serializer.save(usuario=user)
