#!/bin/sh

until timeout 10s celery -A project.celery:app inspect ping; do
    >&2 echo "Celery workers not available"
done

echo 'Starting flower'
celery -A project.celery:app flower
