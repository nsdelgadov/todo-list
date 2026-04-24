# todo-list

Aplicación web "To Do list" construida de forma incremental con Django (backend)
y React (frontend), con tests unitarios y tests de interfaz con Selenium
siguiendo metodología BDD.

## Estado actual

- Backend Django expone `GET /api/tasks/` con el modelo `Task` (title, done,
  created_at) usando Django REST Framework.
- Frontend React muestra `"React OK"` (aún no consume la API — eso llega en
  el siguiente PR).
- Tests unitarios en ambos lados. BDD con Gherkin + Selenium entra en el
  PR donde React empiece a consumir la API.

## Requisitos

- [pixi](https://pixi.sh) instalado (gestor de entornos usado en este proyecto).
  Ningún `pip install`, `venv`, `conda` o `nvm` es necesario — pixi resuelve
  Python, Node y todo lo demás a partir de `pixi.toml` y `pixi.lock`.

## Instalación

```bash
pixi install                # resuelve Python + Node y paquetes conda
pixi run frontend-install   # ejecuta 'npm install' dentro de frontend/
```

## Backend (Django + DRF)

Aplicar migraciones (crea `db.sqlite3` local con las tablas):

```bash
pixi run python manage.py migrate
```

Crear un usuario admin para poder cargar tareas a mano desde `/admin/`:

```bash
pixi run python manage.py createsuperuser
```

Levantar el servidor de desarrollo:

```bash
pixi run python manage.py runserver
```

Abre:
- `http://127.0.0.1:8000/` → `Django OK` (endpoint de salud del app `core`)
- `http://127.0.0.1:8000/admin/` → panel admin, sección **Tasks** para crear/editar
- `http://127.0.0.1:8000/api/tasks/` → endpoint REST (ver sección API abajo)

Tests unitarios:

```bash
pixi run pytest
```

## API

### `GET /api/tasks/`

Devuelve todas las tareas ordenadas de más nueva a más vieja.

Respuesta (200):

```json
[
  {
    "id": 2,
    "title": "Walk the dog",
    "done": false,
    "created_at": "2026-04-24T19:15:03.123Z"
  },
  {
    "id": 1,
    "title": "Buy milk",
    "done": true,
    "created_at": "2026-04-24T18:55:10.456Z"
  }
]
```

Campos:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | int | PK autogenerado (read-only). |
| `title` | string | Texto de la tarea (máx 200 chars). |
| `done` | bool | Si está marcada como hecha. Default `false`. |
| `created_at` | ISO-8601 datetime | Timestamp de creación (read-only). |

Endpoints de creación/edición/borrado aún no existen — llegan en PR #4+.

## Frontend (React + Vite)

Levantar el dev server de Vite en `http://localhost:5173/`:

```bash
pixi run frontend-dev
```

Tests unitarios (vitest + React Testing Library + jsdom):

```bash
pixi run frontend-test
```

## Estructura

```
todo-list/
├── manage.py              # CLI de Django
├── pixi.toml / pixi.lock  # dependencias de backend y node
├── pytest.ini             # configuración de pytest + pytest-django
├── todolist/              # paquete de configuración Django
│   ├── settings.py        # INSTALLED_APPS incluye rest_framework, core, tasks
│   └── urls.py            # /admin/, /api/ (tasks), '' (core)
├── core/                  # app de salud (health check)
│   ├── views.py           # '/' → "Django OK"
│   └── tests/
├── tasks/                 # app del dominio To-Do
│   ├── models.py          # Task(title, done, created_at)
│   ├── serializers.py     # TaskSerializer (DRF)
│   ├── views.py           # TaskViewSet (ReadOnlyModelViewSet por ahora)
│   ├── urls.py            # DefaultRouter → /tasks/
│   ├── admin.py           # registro en /admin/
│   ├── migrations/
│   └── tests/
│       ├── test_models.py
│       └── test_views.py
└── frontend/              # app React (Vite)
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── App.jsx        # renderiza "React OK"
        ├── App.test.jsx
        ├── main.jsx
        └── test-setup.js
```

## Backend y frontend en paralelo

Durante desarrollo corren en dos servidores separados (Django :8000 y
Vite :5173). El frontend aún no consume la API — esa integración llega
en el siguiente PR, junto con los primeros tests BDD en Gherkin + Selenium.
