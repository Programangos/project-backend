# SISA — Backend

Backend del proyecto SISA (Sistema de Supervivencia Académica), desarrollado con Python, Django y Django REST Framework sobre PostgreSQL.

## Requisitos

- Python 3.12+
- Docker y Docker Compose

## Inicialización

Clona el repositorio y ejecuta el script de configuración:

**Linux / macOS:**
```bash
bash setup.sh
```

**Windows:**
```bat
setup.bat
```

El script se encarga de levantar la base de datos, instalar dependencias, aplicar migraciones y lanzar el servidor.

## Estructura del proyecto

```
src/
├── core/
│   ├── controllers/       # API endpoints (APIView)
│   ├── domain/            # Modelos mapeados a tablas existentes (managed = False)
│   ├── infra/             # Repositorios (acceso a datos)
│   ├── serializers/       # Serializadores DRF
│   ├── services/          # Lógica de negocio
│   └── tests/             # Pruebas unitarias
├── sisa/                  # Configuración de Django (settings, urls raíz)
└── manage.py
```

## Ejecutar pruebas

```bash
pytest -v
```

Con cobertura:

```bash
coverage run -m pytest -v
coverage report -m
coverage html
```

## Analizador estático (linter)

```bash
flake8 src/ --max-line-length=100
```