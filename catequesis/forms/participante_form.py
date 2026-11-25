from django import forms
from catequesis.models.participante import Participante


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = [
            'nombres', 'apellidos', 'cedula',
            'fecha_nacimiento', 'telefono', 'representante',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date'}, format='%Y-%m-%d'),
        }