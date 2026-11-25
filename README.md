# Control de Curso de Sacramentos

Aplicación web en Django para administrar los cursos de sacramentos de una parroquia católica: sacramentos, catequistas, participantes, cursos e inscripciones, con control de acceso por grupos de usuarios.

Autora: Elizabeth Placencia


## Requisitos

- Python 3.10 o superior
- Git

## Instalación y ejecución

```bash
git clone <https://github.com/Anahi99/Proyecto_Curso_Iglesia.git>

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_datos
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/` en el navegador.

`cargar_datos` crea los grupos, los usuarios de prueba y al menos 5 registros por tabla. Se puede ejecutar varias veces sin duplicar datos.

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | Admin12345 | Superusuario (también entra a `/admin/`) |
| administrador1 | Admin12345 | Grupo administradores |
| secretaria1 | Secre12345 | Grupo secretaria |

Los usuarios que se registran desde `/registro/` quedan en el grupo secretaria.

## Grupos y permisos

| Grupo | Puede | No puede |
|-------|-------|----------|
| administradores | Crear, editar, eliminar y ver las 5 entidades | — |
| secretaria | Ver todas las entidades, crear inscripciones, y editar o eliminar las inscripciones que ella creó | Crear, editar o eliminar cursos; modificar inscripciones de otros usuarios |

Las vistas están protegidas con `@login_required` y `@permission_required`, y los botones se ocultan en las plantillas según `perms`. Los grupos se crean con `python manage.py crear_grupos`, comando que `cargar_datos` ya ejecuta.

## Entidades

- **Sacramento**: tipo de sacramento y edad mínima.
- **Catequista**: personas que dictan los cursos.
- **Participante**: personas que se inscriben.
- **Curso**: pertenece a un sacramento, tiene varios catequistas (ManyToMany), fechas, cupo, costo y estado.
- **Inscripción**: une un participante con un curso (única por pareja) y guarda quién la creó.

CRUD completo en Curso e Inscripción; listado y detalle en las otras tres. Todas las vistas son vistas de función.

## Estructura

```
config/                  configuración del proyecto
catequesis/
    models/  forms/  views/  urls/     un archivo por entidad
    templates/catequesis/              una carpeta por entidad
    management/commands/               crear_grupos, cargar_datos
```

## Pruebas

```bash
python manage.py test
```