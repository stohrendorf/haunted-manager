This is the backend part of the "Haunted Manager".

## Configuration

Make a copy of `.env.dev` and configure as you please.

## Development

This project uses `poetry`, is based on `django`, and requires Python 3.10 or later.

Tests are using `pytest`, with some type checking done using `pytest --mypy`.

Coding style is ensured and prescribed using `black` and `isort`, while `flake8` enforces even more rules (as long as
one remembers to run all these tools).

## Running

To run this server for the frontend, have a look at what's inside [./entrypoint.sh](entrypoint.sh). You man want to
replace the `gunicorn` call with a call to `manage.py runserver 8000` for local testing.

## Deployment

> ***Do not blindly copy the following commands or configuration values!***

For deploying this backend on a production system, build the `Dockerfile` and tag it. Once it's built, deploy it using
a command like the following one. Don't forget to link to the database container (if any) and name it (so you can
properly) stop the container.

Ensure that the server directory containing publicly accessible files contains a `static` directory, and that the public
web server is allowed to read the files written from the docker container.

```shell
docker run -d --cpus 2 --memory 250m --restart unless-stopped \
  --publish 127.0.0.1:8000:8000 \
  -v ${BACKEND_CONFIG_ENV_FILE}:/etc/haunted-manager/env.prod:ro \
  -v ${PUBLIC_SERVER_FILE_ROOT}/static:/usr/local/haunted-manager/static \
  -e ENV_PATH=/etc/haunted-manager/$(basename ${BACKEND_CONFIG_ENV_FILE}) \
  ${BACKEND_IMAGE_TAG}
```

Once the server is running, ensure your publicly running web server is reverse-proxying any request that starts with
`/api/`, `/email/` or `/admin/` to `localhost:8000`.

For the apache2 web server, this can be achieved with the following lines (ensure you replace the public hostname with
yours):
```
RewriteEngine on
RewriteCond  %{HTTP_HOST}%{REQUEST_URI}  ^haunted\.earvillage\.net/(admin|email|api)/.*$ [NC]
RewriteRule  ^/(.*)$ http://localhost:8000/$1  [proxy]
```

For this to work, your production `env` file (called `${BACKEND_CONFIG_ENV_FILE}` above) should contain the following
configuration (again, replace the hostname with your own one):
```
ALLOWED_HOSTS=localhost,haunted.earvillage.net
CSRF_TRUSTED_ORIGINS=https://haunted.earvillage.net,http://127.0.0.1:8000,http://localhost:8000
CORS_ALLOWED_ORIGINS=https://haunted.earvillage.net,http://127.0.0.1:8000,http://localhost:8000
EMAIL_PAGE_DOMAIN=https://haunted.earvillage.net
```

You can now start your `haunted-coop` instance with
`--manager-url https://haunted.earvillage.net --manager-api-key ${SESSION_CHECK_API_KEY}` to connect to the backend.

Follow the official `django` documentation for creating the initial admin user using `createsuperuser`. Then head over
to the `/admin/` page and add some session tags as you please.
