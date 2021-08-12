#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django import forms

from proagro.models import Comunicado, Cultura


class ComunicadoForm(forms.ModelForm):
    cultura = forms.ModelChoiceField(queryset=Cultura.objects.all().order_by('nome'),
                                     help_text="Selecione a cultura",
                                     widget=forms.Select(attrs={
                                         "class": "form-control",
                                         "data-toggle": "select"
                                     },

                                     ))

    class Meta:
        model = Comunicado
        fields = ['cpf', 'nome', 'email', 'latitude', 'longitude', 'cultura', 'datacolheita', 'evento']
        widgets = {
            'cpf': forms.TextInput(
                attrs={
                    "placeholder": "CPF",
                    "class": "form-control"
                }),
            'nome': forms.TextInput(
                attrs={
                    "placeholder": "Nome",
                    "class": "form-control"
                }),
            'latitude': forms.NumberInput(
                attrs={
                    "placeholder": "-23.123",
                    "class": "form-control"
                }),
            'longitude': forms.NumberInput(
                attrs={
                    "placeholder": "-52.123",
                    "class": "form-control"
                }),
            'email': forms.EmailInput(
                attrs={
                    "placeholder": "nome@email.com",
                    "class": "form-control"
                }),
            'datacolheita': forms.DateInput(format=('%d/%m/%Y'),
                                            attrs={'placeholder': '20/12/2021',
                                                   'class': 'form-control datepicker',
                                                   'data-date-format': 'dd/mm/yyyy'}),
            'evento': forms.Select(
                attrs={
                    "placeholder": "Tipo",
                    "class": "form-control"
                },

                choices=Comunicado.EVENTO_CHOISE
            )
        }
