#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic
from view_breadcrumbs import ListBreadcrumbMixin

from proagro.forms import ComunicadoForm
from proagro.models import Comunicado


class ProagroIndex(LoginRequiredMixin, ListBreadcrumbMixin, generic.ListView):
    paginate_by = 10

    @cached_property
    def crumbs(self):
        return [("Proagro", reverse('proagro:index')), ("Comunicação", '')]

    def get_queryset(self):
        queryset = Comunicado.objects.all()
        if self.request.GET.get("pesquisa"):
            pesquisa = self.request.GET.get("pesquisa")
            if len(pesquisa) > 1:
                queryset = Comunicado.objects.filter(cpf__icontains=pesquisa) | Comunicado.objects.filter(
                    nome__icontains=pesquisa)

        return queryset.order_by('-datacolheita')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get("pesquisa"):
            context['pesquisa'] = self.request.GET.get("pesquisa")

        return context


class ComunicadoCreate(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Comunicado
    form_class = ComunicadoForm
    success_message = "Salvo"

    def form_valid(self, form):
        comunicado = form.save(commit=False)
        comunicado.usuario = self.request.user
        comunicado.save()
        return super().form_valid(form)


class ComunicadoUpdate(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Comunicado
    form_class = ComunicadoForm
    success_message = "Salvo"

    def form_valid(self, form):
        comunicado = form.save(commit=False)
        comunicado.usuario = self.request.user
        comunicado.save()
        return super().form_valid(form)


class ComunicadoDetail(LoginRequiredMixin, generic.DetailView):
    model = Comunicado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.divergente():
            messages.warning(self.request, 'Atenção: Evento Divergente')

        return context

    def get_queryset(self):
        queryset = super(ComunicadoDetail, self).get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return queryset.filter(id=pk).select_related('cultura')


@login_required()
def delete(request, pk):
    Comunicado.objects.get(id=pk).delete()
    messages.success(request, 'Deletado')
    return redirect('proagro:index')
