#!/bin/sh

echo "Чекаємо на PostgreSQL..."

until pg_isready -h db -p 5432 -U home; do
  echo "PostgreSQL не доступний, чекаємо..."
  sleep 2
done

echo "PostgreSQL запущено"

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/products/all.json
python manage.py collectstatic --noinput

exec "$@"