# todo-list

Aplicación web "To Do list" construida de forma incremental con Django (backend)
y React (frontend), con tests unitarios y tests de interfaz con Selenium
siguiendo metodología BDD.

Este PR establece el esqueleto Django mínimo. React, el modelo `Task` y los
tests BDD/Selenium llegan en PRs posteriores.

## Requisitos

- [pixi](https://pixi.sh) instalado (gestor de entornos usado en este proyecto).
  Ningún `pip install`, `venv` o `conda` es necesario — pixi resuelve todo
  a partir de `pixi.toml` y `pixi.lock`.

## Instalación

```bash
pixi install
```

Esto crea el entorno en `.pixi/` (ignorado por git) con Python 3.12, Django 6,
pytest y pytest-django según la versión exacta fijada en `pixi.lock`.

## Uso

Aplicar migraciones (crea `db.sqlite3` local):

```bash
pixi run python manage.py migrate
```

Levantar el servidor de desarrollo:

```bash
pixi run python manage.py runserver
```

Luego abre http://127.0.0.1:8000/ — deberías ver `Django OK`.

## Tests

```bash
pixi run pytest
```

## Estructura

```
todo-list/
├── manage.py              # CLI de Django
├── pixi.toml / pixi.lock  # dependencias (equivalente a requirements.txt)
├── pytest.ini             # configuración de pytest + pytest-django
├── todolist/              # paquete de configuración del proyecto
│   ├── settings.py
│   ├── urls.py            # incluye core.urls en la raíz
│   └── ...
└── core/                  # app principal
    ├── views.py           # index → "Django OK"
    ├── urls.py
    └── tests/             # tests unitarios (pytest)
        └── test_views.py
```
