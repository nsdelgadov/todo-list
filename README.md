# todo-list

Aplicación web "To Do list" construida de forma incremental con Django (backend)
y React (frontend), con tests unitarios y tests de interfaz con Selenium
siguiendo metodología BDD.

Este repo contiene el backend Django mínimo y un frontend React mínimo
que renderiza "React OK". El modelo `Task`, el CRUD y los tests
BDD/Selenium llegan en PRs posteriores.

## Requisitos

- [pixi](https://pixi.sh) instalado (gestor de entornos usado en este proyecto).
  Ningún `pip install`, `venv`, `conda` o `nvm` es necesario — pixi resuelve
  Python, Node y todo lo demás a partir de `pixi.toml` y `pixi.lock`.

## Instalación

```bash
pixi install                # resuelve Python + Node y paquetes conda
pixi run frontend-install   # ejecuta 'npm install' dentro de frontend/
```

## Backend (Django)

Aplicar migraciones (crea `db.sqlite3` local):

```bash
pixi run python manage.py migrate
```

Levantar el servidor de desarrollo en `http://127.0.0.1:8000/`:

```bash
pixi run python manage.py runserver
```

Tests unitarios (pytest + pytest-django):

```bash
pixi run pytest
```

## Frontend (React + Vite)

Levantar el dev server de Vite en `http://localhost:5173/`:

```bash
pixi run frontend-dev
```

Tests unitarios (vitest + React Testing Library + jsdom):

```bash
pixi run frontend-test
```

Build de producción (genera `frontend/dist/`):

```bash
pixi run --manifest-path pixi.toml npm --prefix frontend run build
```

## Estructura

```
todo-list/
├── manage.py              # CLI de Django
├── pixi.toml / pixi.lock  # dependencias de backend y node
├── pytest.ini             # configuración de pytest + pytest-django
├── todolist/              # paquete de configuración Django
│   ├── settings.py
│   └── urls.py            # incluye core.urls en la raíz
├── core/                  # app Django principal
│   ├── views.py           # index → "Django OK"
│   ├── urls.py
│   └── tests/             # tests unitarios (pytest)
│       └── test_views.py
└── frontend/              # app React (Vite)
    ├── package.json       # dependencias npm (gestionadas dentro de frontend/)
    ├── vite.config.js     # config de Vite + Vitest
    ├── index.html
    └── src/
        ├── App.jsx        # renderiza "React OK"
        ├── App.test.jsx   # test unitario con RTL
        ├── main.jsx
        └── test-setup.js  # registra matchers de jest-dom en vitest
```

## Backend y frontend en paralelo

Durante desarrollo corren en dos servidores separados (Django :8000 y
Vite :5173). Todavía no están integrados — eso llega cuando el frontend
empiece a consumir la API del backend en PRs siguientes.
