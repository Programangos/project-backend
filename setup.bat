@echo off
REM Bloque 1: Verificacion del entorno

echo Verificando dependencias del sistema...
docker --version
docker compose version
python --version


REM Bloque 2: Levantar la base de datos

echo Levantando el contenedor de PostgreSQL...
docker compose up -d


REM Bloque 3: Instalar dependencias de Python

echo Creando entorno virtual e instalando dependencias...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt


REM Bloque 4: Configurar Django

echo Aplicando migraciones de Django...
cd src
python manage.py migrate


REM Bloque 5: Pruebas basicas (a expandir en futuras entregas)

echo Ejecutando pruebas basicas...
python manage.py test


REM Bloque 6: Levantar el servidor de desarrollo

echo Levantando el servidor de desarrollo...
python manage.py runserver
