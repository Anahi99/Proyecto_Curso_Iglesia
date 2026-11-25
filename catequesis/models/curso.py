from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Curso(models.Model):
    class Estado(models.TextChoices):
        ABIERTO = 'AB', 'Abierto'
        EN_CURSO = 'EC', 'En curso'
        FINALIZADO = 'FI', 'Finalizado'

    nombre = models.CharField(max_length=100)
    sacramento = models.ForeignKey(
        'catequesis.Sacramento',
        on_delete=models.PROTECT,
        related_name='cursos',
    )
    catequistas = models.ManyToManyField(
        'catequesis.Catequista',
        related_name='cursos',
        blank=True,
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cupo = models.PositiveIntegerField(default=30)
    costo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=2, choices=Estado.choices, default=Estado.ABIERTO
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='cursos_creados',
    )

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('curso_detail', args=[self.pk])