#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from proagro.models import Comunicado


class ProagroIndex(LoginRequiredMixin, generic.ListView):
    paginate_by = 20
    model = Comunicado
