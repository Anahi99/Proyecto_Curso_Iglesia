from datetime import date

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from catequesis.models import Sacramento, Curso, Participante, Inscripcion


class AccesoTests(TestCase):
    def setUp(self):
        call_command('crear_grupos')
        self.admin = User.objects.create_user('adm', password='clave12345')
        self.admin.groups.add(Group.objects.get(name='administradores'))
        self.sec = User.objects.create_user('sec', password='clave12345')
        self.sec.groups.add(Group.objects.get(name='secretaria'))

        sacramento = Sacramento.objects.create(nombre='PC', edad_minima=8)
        curso = Curso.objects.create(
            nombre='Curso de prueba', sacramento=sacramento,
            fecha_inicio=date(2026, 1, 1), fecha_fin=date(2026, 2, 1),
            creado_por=self.admin)
        participante = Participante.objects.create(
            nombres='Ana', apellidos='Mora', cedula='1',
            fecha_nacimiento=date(2015, 1, 1))
        self.inscripcion = Inscripcion.objects.create(
            participante=participante, curso=curso, creado_por=self.admin)

    def test_anonimo_es_enviado_al_login(self):
        respuesta = self.client.get(reverse('curso_create'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/login/', respuesta.url)

    def test_id_inexistente_da_404(self):
        respuesta = self.client.get(reverse('curso_detail', args=[999]))
        self.assertEqual(respuesta.status_code, 404)

    def test_secretaria_no_puede_crear_cursos(self):
        self.client.login(username='sec', password='clave12345')
        respuesta = self.client.get(reverse('curso_create'))
        self.assertEqual(respuesta.status_code, 403)

    def test_administrador_puede_crear_cursos(self):
        self.client.login(username='adm', password='clave12345')
        respuesta = self.client.get(reverse('curso_create'))
        self.assertEqual(respuesta.status_code, 200)

    def test_secretaria_no_edita_inscripcion_ajena(self):
        self.client.login(username='sec', password='clave12345')
        respuesta = self.client.get(
            reverse('inscripcion_edit', args=[self.inscripcion.pk]))
        self.assertEqual(respuesta.status_code, 403)

    def test_logout_solo_por_post(self):
        self.client.login(username='sec', password='clave12345')
        respuesta = self.client.get(reverse('logout'))
        self.assertEqual(respuesta.status_code, 405)