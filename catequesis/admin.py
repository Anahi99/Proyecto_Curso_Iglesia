from django.contrib import admin

from catequesis.models import (
    Sacramento, Catequista, Participante, Curso, Inscripcion,
)


@admin.register(Sacramento)
class SacramentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad_minima')
    list_filter = ('nombre',)
    search_fields = ('descripcion',)


@admin.register(Catequista)
class CatequistaAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'telefono', 'correo', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombres', 'apellidos', 'correo')


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'cedula', 'fecha_nacimiento')
    list_filter = ('fecha_nacimiento',)
    search_fields = ('nombres', 'apellidos', 'cedula')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sacramento', 'fecha_inicio', 'fecha_fin',
                    'cupo', 'costo', 'estado')
    list_filter = ('estado', 'sacramento')
    search_fields = ('nombre',)
    filter_horizontal = ('catequistas',)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('participante', 'curso', 'fecha_inscripcion',
                    'estado', 'creado_por')
    list_filter = ('estado', 'curso')
    search_fields = ('participante__nombres', 'participante__apellidos',
                     'curso__nombre')