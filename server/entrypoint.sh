set -eux
poetry run ./manage.py migrate
poetry run ./manage.py createcachetable
poetry run ./manage.py collectstatic --no-input -c
poetry run gunicorn -b 0.0.0.0:8000 --access-logfile - hauntedserver.wsgi
