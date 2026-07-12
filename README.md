# Tree Views

Tree Views is a Django application that serves a small tree-management API and
the compiled Vue frontend in `templates/` and `static/`. The editable frontend
source lives in `frontend_vue/`.

## Requirements

- Python 3.12 or newer
- Node.js 22 or newer
- npm 10 or newer

## Environment

The Django app reads configuration from environment variables. Defaults are
safe for local development.

| Variable | Default | Description |
| --- | --- | --- |
| `SECRET_KEY` | development-only key | Django signing key. Set this in deployed environments. |
| `DEBUG` | `true` | Enables Django debug mode when set to `true`, `1`, `yes`, or `on`. |
| `ALLOWED_HOSTS` | empty | Comma-separated hostnames allowed by Django. |

Copy `.env.example` if you want a local reference file. Django uses SQLite at
`db.sqlite3` for local development.

## Backend setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
python manage.py migrate
```

## Frontend setup

```bash
cd frontend_vue
npm install
```

## Run locally

Build the frontend assets, then run Django:

```bash
cd frontend_vue
npm run build
cd ..
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

For frontend-only iteration:

```bash
cd frontend_vue
npm run serve
```

## Test and coverage

Run the Django test suite with coverage:

```bash
coverage run --source=core manage.py test
coverage report --fail-under=93
```

Run frontend checks:

```bash
cd frontend_vue
npm run build
npm run lint
```

## Dependency audits

Run dependency audits after installing dependencies:

```bash
python -m pip_audit -r requirements.txt -r requirements-dev.txt
cd frontend_vue
npm audit --audit-level=low
```
