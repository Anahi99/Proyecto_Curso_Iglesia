from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from catequesis.models import (
    Sacramento, Catequista, Participante, Curso, Inscripcion,
)

Tipo = Sacramento.Tipo


class Command(BaseCommand):
    help = 'Crea grupos, usuarios y datos de prueba (se puede repetir sin duplicar)'

    def _usuario(self, username, email, password, grupo=None, superusuario=False):
        user, _ = User.objects.get_or_create(
            username=username, defaults={'email': email})
        user.email = email
        user.set_password(password)
        user.is_staff = superusuario
        user.is_superuser = superusuario
        user.save()
        if grupo:
            user.groups.add(Group.objects.get(name=grupo))
        return user

    def handle(self, *args, **options):
        call_command('crear_grupos')

        # Usuarios de prueba
        admin = self._usuario('admin', 'admin@parroquia.test',
                              'Admin12345', superusuario=True)
        administrador = self._usuario('administrador1', 'administrador1@parroquia.test',
                                      'Admin12345', grupo='administradores')
        secretaria = self._usuario('secretaria1', 'secretaria1@parroquia.test',
                                   'Secre12345', grupo='secretaria')

        # Sacramentos (5)
        sacramentos = {}
        for tipo, descripcion, edad in [
            (Tipo.BAUTISMO, 'Ingreso a la vida cristiana', 0),
            (Tipo.RECONCILIACION, 'Sacramento del perdón', 7),
            (Tipo.PRIMERA_COMUNION, 'Primera participación en la Eucaristía', 8),
            (Tipo.CONFIRMACION, 'Fortalecimiento de la fe', 12),
            (Tipo.MATRIMONIO, 'Preparación para el matrimonio cristiano', 18),
        ]:
            sacramentos[tipo], _ = Sacramento.objects.get_or_create(
                nombre=tipo,
                defaults={'descripcion': descripcion, 'edad_minima': edad})

        # Catequistas (5)
        catequistas = []
        for nombres, apellidos, telefono, correo in [
            ('María', 'Pérez', '0991111111', 'maria.perez@parroquia.test'),
            ('José', 'Granda', '0992222222', 'jose.granda@parroquia.test'),
            ('Lucía', 'Torres', '0993333333', 'lucia.torres@parroquia.test'),
            ('Carlos', 'Vega', '0994444444', 'carlos.vega@parroquia.test'),
            ('Rosa', 'Almeida', '0995555555', 'rosa.almeida@parroquia.test'),
        ]:
            catequista, _ = Catequista.objects.get_or_create(
                nombres=nombres, apellidos=apellidos,
                defaults={'telefono': telefono, 'correo': correo})
            catequistas.append(catequista)

        # Participantes (6)
        participantes = {}
        for cedula, nombres, apellidos, nacimiento, representante in [
            ('1700000001', 'Luis', 'Andrade', date(2016, 3, 10), 'Marta Andrade'),
            ('1700000002', 'Ana', 'Mora', date(2015, 7, 21), 'Pedro Mora'),
            ('1700000003', 'Diego', 'Salazar', date(2012, 1, 15), 'Elena Salazar'),
            ('1700000004', 'Camila', 'Reyes', date(2010, 11, 2), 'Jorge Reyes'),
            ('1700000005', 'Mateo', 'Cruz', date(2017, 5, 30), 'Sandra Cruz'),
            ('1700000006', 'Valeria', 'Núñez', date(1998, 9, 12), ''),
        ]:
            participantes[cedula], _ = Participante.objects.get_or_create(
                cedula=cedula,
                defaults={'nombres': nombres, 'apellidos': apellidos,
                          'fecha_nacimiento': nacimiento,
                          'representante': representante})

        # Cursos (5)
        cursos = {}
        for nombre, tipo, inicio, fin, cupo, costo, estado, indices in [
            ('Catequesis de Bautismo 2026', Tipo.BAUTISMO,
             date(2026, 3, 1), date(2026, 4, 15), 20, '0.00', 'FI', [0]),
            ('Reconciliación Infantil 2026', Tipo.RECONCILIACION,
             date(2026, 5, 4), date(2026, 6, 30), 25, '5.00', 'FI', [1, 2]),
            ('Primera Comunión 2026', Tipo.PRIMERA_COMUNION,
             date(2026, 9, 7), date(2027, 2, 28), 30, '15.00', 'EC', [0, 1]),
            ('Confirmación Juvenil 2026', Tipo.CONFIRMACION,
             date(2026, 9, 14), date(2027, 3, 31), 25, '20.00', 'EC', [3]),
            ('Curso Prematrimonial 2027', Tipo.MATRIMONIO,
             date(2027, 1, 18), date(2027, 3, 1), 15, '30.00', 'AB', [4, 2]),
        ]:
            curso, creado = Curso.objects.get_or_create(
                nombre=nombre,
                defaults={'sacramento': sacramentos[tipo],
                          'fecha_inicio': inicio, 'fecha_fin': fin,
                          'cupo': cupo, 'costo': Decimal(costo),
                          'estado': estado, 'creado_por': admin})
            if creado:
                curso.catequistas.set([catequistas[i] for i in indices])
            cursos[nombre] = curso

        # Inscripciones (7)
        for cedula, curso_nombre, estado, creador in [
            ('1700000001', 'Primera Comunión 2026', 'AC', secretaria),
            ('1700000002', 'Primera Comunión 2026', 'AC', secretaria),
            ('1700000005', 'Primera Comunión 2026', 'PE', administrador),
            ('1700000003', 'Confirmación Juvenil 2026', 'AC', secretaria),
            ('1700000004', 'Confirmación Juvenil 2026', 'AC', administrador),
            ('1700000006', 'Curso Prematrimonial 2027', 'PE', secretaria),
            ('1700000005', 'Reconciliación Infantil 2026', 'AP', administrador),
        ]:
            Inscripcion.objects.get_or_create(
                participante=participantes[cedula],
                curso=cursos[curso_nombre],
                defaults={'estado': estado, 'creado_por': creador})

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados correctamente.'))