from django import forms
from catequesis.models.catequista import Catequista


class CatequistaForm(forms.ModelForm):
    class Meta:
        model = Catequista
        fields = ['nombres', 'apellidos', 'telefono', 'correo', 'activo']