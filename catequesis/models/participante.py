from django.db import models
from django.urls import reverse


class Participante(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, blank=True)
    representante = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'participante'
        verbose_name_plural = 'participantes'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

    def get_absolute_url(self):
        return reverse('participante_detail', args=[self.pk])