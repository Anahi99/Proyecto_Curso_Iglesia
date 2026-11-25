from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Inscripcion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PE', 'Pendiente'
        ACTIVA = 'AC', 'Activa'
        APROBADO = 'AP', 'Aprobado'
        RETIRADO = 'RE', 'Retirado'

    participante = models.ForeignKey(
        'catequesis.Participante',
        on_delete=models.PROTECT,
        related_name='inscripciones',
    )
    curso = models.ForeignKey(
        'catequesis.Curso',
        on_delete=models.CASCADE,
        related_name='inscripciones',
    )
    fecha_inscripcion = models.DateField(default=timezone.localdate)
    estado = models.CharField(
        max_length=2, choices=Estado.choices, default=Estado.PENDIENTE
    )
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='inscripciones_creadas',
    )

    class Meta:
        ordering = ['-fecha_inscripcion']
        verbose_name = 'inscripción'
        verbose_name_plural = 'inscripciones'
        constraints = [
            models.UniqueConstraint(
                fields=['participante', 'curso'],
                name='inscripcion_unica_por_curso',
            )
        ]

    def __str__(self):
        return f'{self.participante} - {self.curso}'

    def get_absolute_url(self):
        return reverse('inscripcion_detail', args=[self.pk])