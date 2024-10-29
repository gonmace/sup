#!/bin/sh

# Espera a que el contenedor de PostgreSQL esté disponible en el puerto 5432
while ! nc -z sup-db 5432; do
  echo "Esperando a que PostgreSQL arranque..."
  sleep 1
done

echo "PostgreSQL está listo"

# Ejecutar Gunicorn después de que PostgreSQL esté listo
exec uvicorn config.asgi:application --host 0.0.0.0 --port 8000

exec "$@"
