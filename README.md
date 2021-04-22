# Cleaning Service Rest Api App
The service uses the following technologies:

- `Python 3.8`
- `Django 3.2`
- `Huey (task queue)`
- `Gunicorn`
- `NGINX 1.19`
- `PostgreSQL 12.4`
- `Redis 6.0.9`
- `Docker`
- `django_rest_framwork 3.12.4`
- `dj_rest_auth 2.1.4`
- `django-allauth 0.44.0`
- `drf-yasg 1.20.0`

## How to run production environment via docker

Use `docker-compose up --build -d` for pull images and start

---

## How to run local development environment  

Use `git pull origin main` for pull the project.
Install requirements for the project from file `requirements.txt`.
Make migrations und load the dump from file dump.json.

---

### Environment variables

| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `DEBUG`  | DEBUG  | True |
| `SECRET_KEY`  | SECRET_KEY  | django-insecure-x31-kaqi+!s0%%x3btymlzah6d8etw1a+)d^i)14bw1s#i-f)l |
| `POSTGRES_USER`  | Postgres username |   cleaning_user   |
| `POSTGRES_PASSWORD`  | Postgres password |  cleaning123    |
| `POSTGRES_DB`  | Postgres database name | cleaning|
| `POSTGRES_HOST`  | Postgres host | 127.0.0.1 |
| `POSTGRES_PORT`  | Postgres port | 5432 |
| `REDIS_URL`  | Redis url | redis://127.0.0.1:6379/0 |
