#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignUpForm


def register_user(request):
    form = SignUpForm(request.POST or None)
    msg = None
    success = False
    a = LoginView.as_view()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = f'User created - please <a href="{reverse("login")}">login</a>.'
            success = True
            messages.success(request, 'Usuário Criado')

            return redirect(reverse('proagro:index'))

        else:
            msg = 'Form is not valid'

    return render(request, "registration/register.html", {"form": form, "msg": msg, "success": success})
