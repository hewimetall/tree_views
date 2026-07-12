# frontend_vue

Vue source for the Django-served Tree Views frontend.

## Setup

```bash
npm install
```

## Run in development

```bash
npm run serve
```

The development server proxies API requests to Django when Django is running on
<http://127.0.0.1:8000/>.

## Build production assets

```bash
npm run build
```

The build writes compiled assets to the repository-level `static/` directory
and `templates/index.html`, where Django serves them.

## Lint

```bash
npm run lint
```

## Audit dependencies

```bash
npm audit --audit-level=low
```
