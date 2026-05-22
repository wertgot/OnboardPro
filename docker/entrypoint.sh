#!/bin/sh
set -e

echo "Waiting for database..."
python - <<'PY'
import os, sys, time
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onboardpro.settings')
django.setup()
from django.db import connection
for i in range(30):
    try:
        connection.ensure_connection()
        break
    except Exception:
        time.sleep(1)
else:
    sys.exit('Database unavailable')
PY

python manage.py migrate --noinput
python manage.py seed_demo
python manage.py collectstatic --noinput

exec "$@"
