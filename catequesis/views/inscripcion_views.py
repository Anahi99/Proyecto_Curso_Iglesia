from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from catequesis.forms.inscripcion_form import InscripcionForm
from catequesis.models.inscripcion import Inscripcion


def _puede_modificar(user, inscripcion):
    """Administradores y superusuario siempre; los demás, solo lo que crearon."""
    return (
        user.is_superuser
        or user.groups.filter(name='administradores').exists()
        or inscripcion.creado_por_id == user.id
    )


def inscripcion_list(request):
    inscripciones = list(
        Inscripcion.objects.select_related('participante', 'curso'))
    for inscripcion in inscripciones:
        inscripcion.puede_modificar = _puede_modificar(request.user, inscripcion)
    return render(request, 'catequesis/inscripciones/lista.html',
                  {'inscripciones': inscripciones})


def inscripcion_detail(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    return render(request, 'catequesis/inscripciones/detalle.html', {
        'inscripcion': inscripcion,
        'puede_modificar': _puede_modificar(request.user, inscripcion),
    })


@login_required
@permission_required('catequesis.add_inscripcion', raise_exception=True)
def inscripcion_create(request):
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.creado_por = request.user
            inscripcion.save()
            messages.success(request, 'Inscripción creada exitosamente.')
            return redirect('inscripcion_list')
    else:
        form = InscripcionForm()
    return render(request, 'catequesis/inscripciones/formulario.html',
                  {'form': form, 'titulo': 'Nueva inscripción'})


@login_required
@permission_required('catequesis.change_inscripcion', raise_exception=True)
def inscripcion_edit(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if not _puede_modificar(request.user, inscripcion):
        raise PermissionDenied
    if request.method == 'POST':
        form = InscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscripción actualizada exitosamente.')
            return redirect('inscripcion_detail', pk=inscripcion.pk)
    else:
        form = InscripcionForm(instance=inscripcion)
    return render(request, 'catequesis/inscripciones/formulario.html',
                  {'form': form, 'titulo': 'Editar inscripción'})


@login_required
@permission_required('catequesis.delete_inscripcion', raise_exception=True)
def inscripcion_delete(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if not _puede_modificar(request.user, inscripcion):
        raise PermissionDenied
    if request.method == 'POST':
        inscripcion.delete()
        messages.success(request, 'Inscripción eliminada exitosamente.')
        return redirect('inscripcion_list')
    return render(request, 'catequesis/inscripciones/confirmar_eliminar.html',
                  {'inscripcion': inscripcion})