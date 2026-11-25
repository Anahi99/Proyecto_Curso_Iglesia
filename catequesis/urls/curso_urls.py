from django.urls import path
from catequesis.views import (
    curso_list, curso_detail, curso_create, curso_edit, curso_delete,
)

urlpatterns = [
    path('cursos/', curso_list, name='curso_list'),
    path('cursos/nuevo/', curso_create, name='curso_create'),
    path('cursos/<int:pk>/', curso_detail, name='curso_detail'),
    path('cursos/<int:pk>/editar/', curso_edit, name='curso_edit'),
    path('cursos/<int:pk>/eliminar/', curso_delete, name='curso_delete'),
]