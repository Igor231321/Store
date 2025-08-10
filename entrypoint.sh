#!/bin/sh

if [ "$POSTGRES_DB" = "store" ]
then
    echo "Запускаємо postgres"

    while ! nc -z "db" $POSTGRES POST; do
      sleep 0.5
    done

    echo "PostgresSQL запущен"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/products/all.json
python manage.py runserver 0.0.0.0:8000