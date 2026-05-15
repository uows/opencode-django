# EduCore 🎓

Plataforma de gestión escolar construida con Django 5. Orientada a colegios y liceos, con perfiles de **Alumno**, **Profesor** y **Administrador**.

---

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 5.0 |
| Frontend | Django Templates + TailwindCSS (CDN) |
| Base de datos | SQLite |
| Autenticación | Sesiones Django |
| Mock data | Faker |

---

## Requisitos

- Python 3.12+
- pip

---

## Instalación y ejecución

```bash
# 1. Clonar o ubicarse en el proyecto
cd educore

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Migrar base de datos
python manage.py migrate

# 4. (Opcional) Cargar datos de prueba
python manage.py seed_data

# 5. Iniciar servidor
python manage.py runserver
```

Abrir `http://localhost:8000/` en el navegador.

---

## Credenciales de prueba (seed)

| Rol | Email | Contraseña |
|---|---|---|
| Administrador | `admin@educore.cl` | `admin123` |
| Profesor | `maria.gonzalez@educore.cl` | `profesor123` |
| Profesor | `carlos.muñoz@educore.cl` | `profesor123` |
| Profesor | `ana.lópez@educore.cl` | `profesor123` |
| Profesor | `pedro.ramírez@educore.cl` | `profesor123` |
| Profesor | `laura.torres@educore.cl` | `profesor123` |
| Alumno | `maria.soto0@educore.cl` ... `nombre.apellido29@educore.cl` | `alumno123` |

> Para ver los emails exactos de alumnos, ejecutar:
> ```bash
> python manage.py shell -c "from apps.accounts.models import User; print('\n'.join([u.email for u in User.objects.filter(role='STUDENT')]))"
> ```

---

## Datos de prueba generados

El comando `seed_data` crea:

| Ítem | Cantidad |
|---|---|
| Administradores | 1 |
| Profesores | 5 |
| Alumnos | 30 |
| Cursos | 6 |
| Asignaturas | 32 |
| Inscripciones | ~44 |
| Notas | ~1074 |
| Tareas | ~58 |

Distribución de cursos: 1° Básico, 2° Básico, 5° Básico, 1° Medio, 2° Medio, 3° Medio.

---

## Roles y permisos

| Rol | Acceso |
|---|---|
| **STUDENT** | Dashboard propio, ver cursos inscritos, ver notas y promedio, ver tareas pendientes, descargar archivos, editar perfil |
| **TEACHER** | Dashboard con estadísticas, CRUD de cursos propios, gestionar asignaturas, inscribir alumnos, registrar/editar notas, crear/editar tareas con PDF, ver rendimiento de alumnos |
| **ADMIN** | Todo lo de TEACHER + acceso al panel de administración Django (`/admin/`), CRUD de usuarios, gestión global de cursos |

---

## Estructura del proyecto

```
educore/
├── manage.py                     # Entry point Django
├── requirements.txt              # Dependencias
├── .env                          # Variables de entorno
├── db.sqlite3                    # Base de datos (SQLite)
├── media/                        # Archivos subidos (PDFs de tareas)
├── static/                       # Archivos estáticos (JS)
├── config/                       # Configuración del proyecto
│   ├── settings.py               # Settings globales
│   ├── urls.py                   # Rutas raíz
│   └── wsgi.py                   # WSGI entry point
├── apps/                         # Aplicaciones Django
│   ├── accounts/                 # Usuarios, autenticación, roles
│   │   ├── models.py             # User (email como username, role)
│   │   ├── views.py              # login, register, dashboard, perfil
│   │   ├── urls.py               # Rutas de accounts
│   │   └── management/
│   │       └── commands/
│   │           └── seed_data.py  # Generador de datos mock
│   ├── courses/                  # Cursos, asignaturas, inscripciones
│   │   ├── models.py             # Course, Subject, Enrollment
│   │   ├── views.py              # CRUD cursos, asignaturas, enroll
│   │   └── urls.py
│   ├── grades/                   # Sistema de notas
│   │   ├── models.py             # Grade (score, coefficient)
│   │   ├── views.py              # Notas por rol, promedios
│   │   └── urls.py
│   └── assignments/              # Tareas con archivos
│       ├── models.py             # Assignment (title, due_date, PDF)
│       ├── views.py              # CRUD tareas
│       └── urls.py
└── templates/                    # Templates Django + TailwindCSS
    ├── base.html                 # Layout base con sidebar responsivo
    ├── components/               # Sidebar, navbar reutilizables
    ├── accounts/                 # login, register, dashboard, perfil
    ├── courses/                  # listado, detalle, formularios
    ├── grades/                   # tabla notas, formularios, gráficos
    └── assignments/              # listado, detalle, formularios
```

---

## Rutas (endpoints)

### Públicas
| URL | Método | Descripción |
|---|---|---|
| `/` o `/login/` | GET/POST | Inicio de sesión |
| `/register/` | GET/POST | Registro de alumno |

### Autenticadas
| URL | Método | Roles | Descripción |
|---|---|---|---|
| `/dashboard/` | GET | Todos | Dashboard con cards según rol |
| `/profile/` | GET/POST | Todos | Editar perfil |
| `/courses/` | GET | Todos | Listar cursos |
| `/courses/new/` | GET/POST | TEACHER/ADMIN | Crear curso |
| `/courses/{id}/` | GET | Todos | Detalle del curso |
| `/courses/{id}/edit/` | GET/POST | TEACHER/ADMIN | Editar curso |
| `/courses/{id}/delete/` | POST | TEACHER/ADMIN | Eliminar curso |
| `/courses/{id}/subjects/new/` | GET/POST | TEACHER/ADMIN | Crear asignatura |
| `/courses/subjects/{id}/edit/` | GET/POST | TEACHER/ADMIN | Editar asignatura |
| `/courses/subjects/{id}/delete/` | POST | TEACHER/ADMIN | Eliminar asignatura |
| `/courses/{id}/enroll/` | GET/POST | TEACHER/ADMIN | Inscribir alumno |
| `/grades/` | GET | Todos | Ver notas (vista según rol) |
| `/grades/new/` | GET/POST | TEACHER/ADMIN | Registrar nota |
| `/grades/{id}/edit/` | GET/POST | TEACHER/ADMIN | Editar nota |
| `/grades/{id}/delete/` | POST | TEACHER/ADMIN | Eliminar nota |
| `/grades/student/{id}/` | GET | TEACHER/STUDENT | Rendimiento del alumno |
| `/assignments/` | GET | Todos | Listar tareas |
| `/assignments/new/` | GET/POST | TEACHER/ADMIN | Crear tarea |
| `/assignments/{id}/` | GET | Todos | Detalle tarea |
| `/assignments/{id}/edit/` | GET/POST | TEACHER/ADMIN | Editar tarea |
| `/assignments/{id}/delete/` | POST | TEACHER/ADMIN | Eliminar tarea |
| `/admin/` | GET/POST | ADMIN | Panel Django admin |

---

## Modelos de datos

### User (accounts)
| Campo | Tipo | Descripción |
|---|---|---|
| email | EmailField (unique) | Usado como username |
| first_name | CharField | Nombre |
| last_name | CharField | Apellido |
| role | CharField (choices) | STUDENT, TEACHER, ADMIN |
| password | CharField | Contraseña hasheada |

### Course (courses)
| Campo | Tipo | Descripción |
|---|---|---|
| name | CharField | Nombre del curso |
| grade | CharField | Grado (1° Básico, 2° Medio, etc.) |
| year | PositiveIntegerField | Año académico |
| teacher | FK → User (TEACHER) | Profesor a cargo |
| created_at | DateTimeField | Fecha de creación |

### Subject (courses)
| Campo | Tipo | Descripción |
|---|---|---|
| name | CharField | Nombre de la asignatura |
| description | TextField | Descripción opcional |
| course | FK → Course | Curso al que pertenece |

### Enrollment (courses)
| Campo | Tipo | Descripción |
|---|---|---|
| student | FK → User (STUDENT) | Alumno |
| course | FK → Course | Curso |
| enrolled_at | DateTimeField | Fecha de inscripción |

### Grade (grades)
| Campo | Tipo | Descripción |
|---|---|---|
| student | FK → User (STUDENT) | Alumno |
| subject | FK → Subject | Asignatura |
| score | Decimal (1.0-7.0) | Nota |
| coefficient | PositiveIntegerField | Coeficiente (default 1) |
| date | DateField | Fecha de registro |

### Assignment (assignments)
| Campo | Tipo | Descripción |
|---|---|---|
| title | CharField | Título de la tarea |
| description | TextField | Descripción |
| subject | FK → Subject | Asignatura |
| due_date | DateTimeField | Fecha de entrega |
| attachment | FileField (PDF) | Archivo adjunto (opcional) |
| created_by | FK → User | Creador de la tarea |
| created_at | DateTimeField | Fecha de creación |

---

## Tecnologías usadas

- **Django 5.0** — Framework web
- **TailwindCSS (CDN)** — Estilos utilitarios
- **Chart.js (CDN)** — Gráficos de promedios
- **Faker** — Generación de datos mock
- **python-decouple** — Variables de entorno
- **SQLite** — Base de datos

---

## Desarrollo

```bash
# Verificar migraciones
python manage.py makemigrations
python manage.py migrate

# Regenerar datos de prueba (borra todo y crea de nuevo)
python manage.py seed_data

# Crear superusuario manual
python manage.py createsuperuser
```

---

## Capturas de pantalla (para referencia)

El proyecto incluye:

- **Login** con diseño centrado, logo y formulario
- **Dashboard** con cards de estadísticas (diferentes por rol)
- **Listado de cursos** en grid de tarjetas
- **Detalle de curso** con asignaturas y alumnos
- **Notas** con tabla filtrable y gráfico Chart.js de promedios
- **Tareas** con indicador de vencidas/activas y descarga de PDF
- **Sidebar responsivo** con navegación contextual por rol
- **Perfil de usuario** editable
