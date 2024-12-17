#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "check if database is running..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done

    echo "The database is up and running :-D"
fi

alembic revision --autogenerate
alembic upgrade head

exec "$@"