#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.urls import include, path
from rest_framework import routers

from api.views import CulturaViewSet, ComunicadoViewSet

router = routers.DefaultRouter()
router.register(r'culturas', CulturaViewSet)
router.register(r'comunicados', ComunicadoViewSet)

urlpatterns = [

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
