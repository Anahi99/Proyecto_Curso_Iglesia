from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

MODELOS = ['sacramento', 'catequista', 'participante', 'curso', 'inscripcion']


class Command(BaseCommand):
    help = 'Crea los grupos administradores y secretaria con sus permisos'

    def handle(self, *args, **options):
        administradores, _ = Group.objects.get_or_create(name='administradores')
        secretaria, _ = Group.objects.get_or_create(name='secretaria')

        permisos_admin = []
        permisos_secretaria = []
        for modelo in MODELOS:
            for accion in ['add', 'change', 'delete', 'view']:
                permisos_admin.append(f'{accion}_{modelo}')
            permisos_secretaria.append(f'view_{modelo}')
        permisos_secretaria += [
            'add_inscripcion', 'change_inscripcion', 'delete_inscripcion',
        ]

        administradores.permissions.set(Permission.objects.filter(
            content_type__app_label='catequesis',
            codename__in=permisos_admin))
        secretaria.permissions.set(Permission.objects.filter(
            content_type__app_label='catequesis',
            codename__in=permisos_secretaria))

        self.stdout.write(self.style.SUCCESS(
            'Grupos administradores y secretaria creados correctamente.'))