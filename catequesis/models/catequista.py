from django.db import models
from django.urls import reverse


class Catequista(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    correo = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'catequista'
        verbose_name_plural = 'catequistas'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

    def get_absolute_url(self):
        return reverse('catequista_detail', args=[self.pk])