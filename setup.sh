#!/bin/bash

# Bloque 1: Verificación del entorno

echo "Verificando dependencias del sistema..."
docker --version
docker compose version
python3 --version


# Bloque 2: Levantar la base de datos

echo "Levantando el contenedor de PostgreSQL..."
docker compose up -d


# Bloque 3: Instalar dependencias de Python

echo "Creando entorno virtual e instalando dependencias..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# Bloque 4: Configurar Django

echo "Aplicando migraciones de Django..."
cd src
python manage.py migrate


# Bloque 5: Pruebas básicas (a expandir en futuras entregas)

echo "Ejecutando pruebas básicas..."
python manage.py test


# Bloque 6: Levantar el servidor de desarrollo

echo "Levantando el servidor de desarrollo..."
python manage.py runserver
