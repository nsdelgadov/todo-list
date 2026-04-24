# todo-list

Aplicación web "To Do list" construida de forma incremental con Django (backend)
y React (frontend), con tests unitarios y tests de interfaz con Selenium
siguiendo metodología BDD.

## Estado actual

- Backend Django expone `GET /api/tasks/` con el modelo `Task` (title, done,
  created_at) usando Django REST Framework.
- Frontend React consume `/api/tasks/` a través del proxy de Vite y renderiza
  la lista con estados de loading / error / empty / list.
- Tests unitarios para el backend (pytest + pytest-django). La cobertura del
  frontend se hace end-to-end con Selenium + BDD (Gherkin) — eso llega en el
  siguiente PR.

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
    "id": "7e3a2b1c-4d5e-6f70-8192-a3b4c5d6e7f8",
    "title": "Walk the dog",
    "done": false,
    "created_at": "2026-04-24T19:15:03.123Z"
  },
  {
    "id": "1a2b3c4d-5e6f-7890-abcd-ef1234567890",
    "title": "Buy milk",
    "done": true,
    "created_at": "2026-04-24T18:55:10.456Z"
  }
]
```

Campos:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUIDv4 string | PK autogenerado (read-only). No enumerable. |
| `title` | string | Texto de la tarea (máx 200 chars). |
| `done` | bool | Si está marcada como hecha. Default `false`. |
| `created_at` | ISO-8601 datetime | Timestamp de creación (read-only). |

Endpoints de creación/edición/borrado aún no existen — llegan en PR #4+.

## Frontend (React + Vite)

Levantar el dev server de Vite en `http://localhost:5173/`:

```bash
pixi run frontend-dev
```

Vite proxea cualquier `/api/*` a `http://localhost:8000`, así que desde el
navegador el fetch es same-origin y no hace falta configurar CORS en Django.
Para verlo en acción tienes que tener **los dos servidores corriendo en
paralelo** (ver [Dev workflow](#dev-workflow-con-dos-servidores)).

No hay tests unitarios de frontend: la cobertura vive en la suite E2E
(Selenium + pytest-bdd, PR siguiente). La infraestructura de vitest sigue
instalada por si algún componente con lógica compleja justifica un test
aislado en el futuro.

## Dev workflow con dos servidores

Abre dos terminales en la raíz del repo.

Terminal 1 — backend:

```bash
pixi run python manage.py runserver
```

Terminal 2 — frontend:

```bash
pixi run frontend-dev
```

Abre `http://localhost:5173/`:

- Si no hay tareas → "No tasks yet"
- Si hay tareas → lista con `[x] title` (done) o `[ ] title` (pendiente)
- Si Django está caído → "Failed to load tasks"
- Brevemente al cargar → "Loading…"

Para poblar tareas crea algunas desde `/admin/` (ver sección de Backend).

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
    ├── vite.config.js     # config + proxy /api → :8000 + vitest
    ├── index.html
    └── src/
        ├── App.jsx        # fetch /api/tasks/ y renderiza lista
        ├── main.jsx
        └── test-setup.js  # setup de vitest (queda para uso futuro)
```
