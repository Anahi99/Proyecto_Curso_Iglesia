from django import forms
from catequesis.models.curso import Curso


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
            'nombre', 'sacramento', 'catequistas',
            'fecha_inicio', 'fecha_fin', 'cupo', 'costo', 'estado',
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(
                attrs={'type': 'date'}, format='%Y-%m-%d'),
        }