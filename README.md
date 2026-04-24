# todo-list

Aplicación web "To Do list" construida de forma incremental con Django (backend)
y React (frontend), con tests unitarios en backend y tests end-to-end con
Selenium + BDD (Gherkin) para el flujo completo.

## Estado actual

- Backend Django expone `GET /api/tasks/` con el modelo `Task` (title, done,
  created_at) usando Django REST Framework. Health check en `GET /health/`.
- Frontend React lista las tareas con estados `loading` / `error` / `empty` /
  `list`. Servido en `/` por Django (build de Vite) o por Vite dev server.
- Tests unitarios para backend con pytest + pytest-django.
- Tests end-to-end con Selenium + pytest-bdd: el primer escenario en
  `e2e/features/view_tasks.feature` cubre la lista vacía y la lista con
  tareas done/no done.

## Requisitos

- [pixi](https://pixi.sh) instalado.
- **Google Chrome** instalado en el sistema (la suite E2E lo usa headless).
  Selenium 4 baja chromedriver automáticamente — no hay que instalarlo a mano.

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

URLs:
- `http://127.0.0.1:8000/` → la SPA de React (si `frontend/dist/` existe; si
  no, un 503 que pide ejecutar `pixi run frontend-build`)
- `http://127.0.0.1:8000/health/` → `Django OK` (health check)
- `http://127.0.0.1:8000/admin/` → panel admin, sección **Tasks**
- `http://127.0.0.1:8000/api/tasks/` → endpoint REST

Tests unitarios (rápidos, sólo backend):

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
  }
]
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUIDv4 string | PK autogenerado (read-only). No enumerable. |
| `title` | string | Texto de la tarea (máx 200 chars). |
| `done` | bool | Si está marcada como hecha. Default `false`. |
| `created_at` | ISO-8601 datetime | Timestamp de creación (read-only). |

## Frontend (React + Vite)

Levantar el dev server de Vite en `http://localhost:5173/`:

```bash
pixi run frontend-dev
```

Vite proxea `/api/*` a `http://localhost:8000`. Para verlo en acción tienes
que tener **los dos servidores corriendo en paralelo** (ver
[Dev workflow](#dev-workflow-con-dos-servidores)).

Build de producción (genera `frontend/dist/`, lo que sirve Django en `/`):

```bash
pixi run frontend-build
```

No hay tests unitarios de frontend: la cobertura vive en la suite E2E.

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

Para poblar tareas crea algunas desde `/admin/`.

## Tests end-to-end (BDD + Selenium)

```bash
pixi run e2e
```

Esto encadena `frontend-build` y luego `pytest e2e/` con Chrome headless.
Tarda unos 10 segundos (los unit tests están separados — esos siguen siendo
sub-segundo con `pixi run pytest`).

### Mini-curso de Gherkin

Cada escenario E2E vive en un archivo `.feature` escrito en lenguaje
**Gherkin** — inglés casi natural. Ejemplo del archivo
`e2e/features/view_tasks.feature`:

```gherkin
Feature: Viewing the task list
  As a user of the app
  I want to see my tasks at a glance with their done state

  Scenario: Tasks are listed with their done state
    Given a task titled "Buy milk" exists and is not done
    And a task titled "Walk the dog" exists and is done
    When I open the app
    Then I see "Buy milk" displayed as not done
    And I see "Walk the dog" displayed as done
```

Palabras clave:

- **Feature** — capacidad del sistema.
- **Scenario** — un ejemplo concreto de esa capacidad.
- **Given** — preconditions: lo que ya existe en el mundo antes de la acción.
- **When** — la acción que se ejecuta.
- **Then** — resultado esperado.
- **And** / **But** — continuación del paso anterior, sin cambiar la fase.

Cada paso (`Given/When/Then`) mapea a una función Python en
`e2e/step_defs/test_view_tasks.py` mediante decoradores de **pytest-bdd**:

```python
@given(parsers.parse('a task titled "{title}" exists and is not done'))
def _given_pending_task(title):
    Task.objects.create(title=title, done=False)

@when("I open the app")
def _when_open_app(browser, live_server):
    browser.get(live_server.url + "/")
```

El placeholder `{title}` extrae el valor entre comillas y lo pasa a la
función como argumento. Así un mismo step def cubre infinitos scenarios con
distintos títulos.

### Por qué BDD

1. **Documentación viva**: el `.feature` describe el comportamiento
   esperado en lenguaje plano y siempre está al día porque es ejecutable.
2. **Pensamiento outside-in**: escribes el escenario antes que el código,
   forzando a pensar en el usuario.
3. **Reutilización de steps**: `Given a task titled "..."` se reusará en los
   PRs de crear/editar/marcar — no rescribirás el setup.

## Estructura

```
todo-list/
├── manage.py              # CLI de Django
├── pixi.toml / pixi.lock  # dependencias backend + node + selenium
├── pytest.ini             # pytest unit (testpaths = core tasks)
├── todolist/              # paquete de configuración Django
│   ├── settings.py
│   └── urls.py            # /admin/, /api/, /assets/<path>, '' (SPA)
├── core/                  # views auxiliares (índice SPA + health check)
│   ├── views.py           # index → React; health → "Django OK"
│   ├── urls.py
│   └── tests/
├── tasks/                 # app del dominio To-Do
│   ├── models.py          # Task(id UUID, title, done, created_at)
│   ├── serializers.py
│   ├── views.py           # TaskViewSet (DRF)
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── tests/
├── frontend/              # app React (Vite)
│   ├── package.json
│   ├── vite.config.js     # proxy /api → :8000 + vitest config
│   ├── index.html
│   ├── dist/              # build de Vite (gitignored)
│   └── src/
│       ├── App.jsx        # fetch /api/tasks/ y renderiza
│       ├── main.jsx
│       └── test-setup.js
└── e2e/                   # suite end-to-end (BDD + Selenium)
    ├── pytest.ini         # config local (pythonpath = ..)
    ├── conftest.py        # fixtures: browser (Chrome), live_server (autouse)
    ├── features/
    │   └── view_tasks.feature
    └── step_defs/
        └── test_view_tasks.py
```
