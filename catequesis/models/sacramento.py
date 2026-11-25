from django.db import models
from django.urls import reverse


class Sacramento(models.Model):
    class Tipo(models.TextChoices):
        BAUTISMO = 'BA', 'Bautismo'
        PRIMERA_COMUNION = 'PC', 'Primera Comunión'
        CONFIRMACION = 'CO', 'Confirmación'
        MATRIMONIO = 'MA', 'Matrimonio'

    nombre = models.CharField(max_length=2, choices=Tipo.choices, unique=True)
    descripcion = models.TextField(blank=True)
    edad_minima = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'sacramento'
        verbose_name_plural = 'sacramentos'

    def __str__(self):
        return self.get_nombre_display()

    def get_absolute_url(self):
        return reverse('sacramento_detail', args=[self.pk])