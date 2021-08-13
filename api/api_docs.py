#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

api_project_description = """
Api Proagro Fácil
"""

schema_url_patterns = [path('api/', include('api.urls')), ]

schema_view = get_schema_view(
    openapi.Info(
        title="Proagro",
        default_version='v1',
        description=f"{api_project_description}",
        contact=openapi.Contact(email="julioriffel@gmail.com")
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns
)

docs_urls = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
