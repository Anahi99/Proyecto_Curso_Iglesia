from django.urls import path
from catequesis.views import (
    inscripcion_list, inscripcion_detail, inscripcion_create,
    inscripcion_edit, inscripcion_delete,
)

urlpatterns = [
    path('inscripciones/', inscripcion_list, name='inscripcion_list'),
    path('inscripciones/nueva/', inscripcion_create, name='inscripcion_create'),
    path('inscripciones/<int:pk>/', inscripcion_detail, name='inscripcion_detail'),
    path('inscripciones/<int:pk>/editar/', inscripcion_edit, name='inscripcion_edit'),
    path('inscripciones/<int:pk>/eliminar/', inscripcion_delete, name='inscripcion_delete'),
]