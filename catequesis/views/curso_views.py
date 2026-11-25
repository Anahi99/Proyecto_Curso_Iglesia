from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from catequesis.forms.curso_form import CursoForm
from catequesis.models.curso import Curso


def curso_list(request):
    cursos = Curso.objects.select_related('sacramento')
    return render(request, 'catequesis/cursos/lista.html', {'cursos': cursos})


def curso_detail(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'catequesis/cursos/detalle.html', {'curso': curso})


@login_required
def curso_create(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.creado_por = request.user
            curso.save()
            form.save_m2m()
            messages.success(request, 'Curso creado exitosamente.')
            return redirect('curso_list')
    else:
        form = CursoForm()
    return render(request, 'catequesis/cursos/formulario.html',
                  {'form': form, 'titulo': 'Nuevo curso'})


@login_required
def curso_edit(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado exitosamente.')
            return redirect('curso_detail', pk=curso.pk)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'catequesis/cursos/formulario.html',
                  {'form': form, 'titulo': 'Editar curso'})


@login_required
def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado exitosamente.')
        return redirect('curso_list')
    return render(request, 'catequesis/cursos/confirmar_eliminar.html',
                  {'curso': curso})