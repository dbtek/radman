#! /usr/bin/env bash

# Let the DB start
echo "Waiting for postgres..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
done

# Run migrations
python manage.py migrate