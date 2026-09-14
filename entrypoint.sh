#!/bin/sh

# Espera a que el contenedor de PostgreSQL esté disponible en el puerto 5432
while ! nc -z sup-db 5432; do
  echo "Esperando a que PostgreSQL arranque..."
  sleep 1
done

echo "PostgreSQL está listo"

# Recolectar estáticos sobre el volumen montado (collectstatic del build queda
# tapado por el bind mount de ./staticfiles, hay que regenerarlo en runtime)
python manage.py collectstatic --noinput --settings=config.prod

# Ejecutar Gunicorn después de que PostgreSQL esté listo
exec uvicorn config.asgi:application --host 0.0.0.0 --port 8000
