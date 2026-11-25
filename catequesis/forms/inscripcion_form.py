from django import forms
from catequesis.models.inscripcion import Inscripcion


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = [
            'participante', 'curso', 'fecha_inscripcion',
            'estado', 'observaciones',
        ]
        widgets = {
            'fecha_inscripcion': forms.DateInput(
                attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean(self):
        cleaned = super().clean()
        participante = cleaned.get('participante')
        curso = cleaned.get('curso')
        estado = cleaned.get('estado')

        if participante and curso:
            # Al editar, se excluye el propio registro de las comprobaciones
            repetidas = Inscripcion.objects.filter(
                participante=participante, curso=curso)
            if self.instance.pk:
                repetidas = repetidas.exclude(pk=self.instance.pk)

            if repetidas.exists():
                self.add_error(
                    'participante',
                    'Este participante ya está inscrito en ese curso.')
            elif estado != Inscripcion.Estado.RETIRADO:
                ocupados = Inscripcion.objects.filter(curso=curso).exclude(
                    estado=Inscripcion.Estado.RETIRADO)
                if self.instance.pk:
                    ocupados = ocupados.exclude(pk=self.instance.pk)
                if ocupados.count() >= curso.cupo:
                    self.add_error(
                        'curso', 'El curso ya alcanzó su cupo máximo.')
        return cleaned