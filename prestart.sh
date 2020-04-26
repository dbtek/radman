#! /usr/bin/env bash

# Let the DB start
sleep 10;

# Run migrations
DJANGO_SETTINGS_MODULE=radman.settings.prod python manage.py migrate