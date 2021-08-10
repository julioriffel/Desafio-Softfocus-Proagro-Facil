#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django import forms

from proagro.models import Comunicado


class ComunicadoForm(forms.ModelForm):
    cpf = forms.CharField(
        attrs={
            "placeholder": "CPF",
            "class": "form-control"
        }
    )
    nome = forms.CharField(
        attrs={
            "placeholder": "Nome",
            "class": "form-control"
        }
    )
    email = forms.EmailField(
        attrs={
            "placeholder": "Nome",
            "class": "form-control"
        }
    )
    latitude = forms.NumberInput(
        attrs={
            "placeholder": "Latitude",
            "class": "form-control",
        })
    longitude = forms.NumberInput(
        attrs={
            "placeholder": "Longitude",
            "class": "form-control"
        })
    datacolheita = forms.DateInput(format=('%d/%m/%Y'),
                                   attrs={'class': 'form-control datepicker',
                                          'data-date-format': 'dd/mm/yyyy'}),
    tipo = forms.CharField(
        widget=forms.Select(
            attrs={
                "placeholder": "Evento",
                "class": "form-control"
            },

            choices=Comunicado.EVENTO_CHOISE
        ))

    # class Meta:
    #     model = Comunicado
    #     fields = ['']
    #     widgets = {
    #         'datacolheita': forms.DateInput(format=('%d/%m/%Y'),
    #                                 attrs={'class': 'form-control datepicker',
    #                                        'data-date-format': 'dd/mm/yyyy'}),
    #     }
