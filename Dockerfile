FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cd src && python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "sisa.wsgi:application", "--bind", "0.0.0.0:8000", "--chdir", "/app/src"]
