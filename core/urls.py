#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
import debug_toolbar
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from api.api_docs import docs_urls

urlpatterns = [
                  path("api/", include("api.urls")),
                  path("conta/", include("conta.urls")),
                  path('admin/', admin.site.urls),
                  path("", include("proagro.urls")),
              ] + docs_urls
urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
