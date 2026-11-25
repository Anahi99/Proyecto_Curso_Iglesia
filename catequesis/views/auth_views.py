from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from catequesis.forms.registro_form import RegistroForm


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo = Group.objects.filter(name='secretaria').first()
            if grupo:
                user.groups.add(grupo)
            auth_login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenida al sistema.')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'catequesis/auth/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, 'Sesión iniciada correctamente.')
            siguiente = request.GET.get('next')
            if siguiente and url_has_allowed_host_and_scheme(
                    siguiente, allowed_hosts={request.get_host()}):
                return redirect(siguiente)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'catequesis/auth/login.html', {'form': form})


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect('login')