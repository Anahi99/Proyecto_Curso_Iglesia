from django import forms
from catequesis.models.sacramento import Sacramento


class SacramentoForm(forms.ModelForm):
    class Meta:
        model = Sacramento
        fields = ['nombre', 'descripcion', 'edad_minima']