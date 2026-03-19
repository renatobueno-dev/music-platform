# Stage 2 - Docker Workflow (Steps A to E)

Stage 2 focuses on portability and reproducibility.
The target is not only "it works on my machine", but "it works the same way in containers."

## Prerequisites

- Docker Desktop (or Docker Engine + Compose) installed and running.
- Project root as current directory:
  - `.../13_checkpoint_nivel_3`

## Step A - Freeze startup logic

Use these values as the source of truth for container runtime:

| Item | Value |
| --- | --- |
| FastAPI entrypoint | `app.main:app` |
| Dependencies file | `requirements.txt` |
| API port (container) | `8000` |
| Runtime command | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |

Checkpoint:
- All Docker/Compose files must respect these same values.

## Step B - Create Dockerfile (API only)

Goal:
- Build an API image that can run independently.

Commands:

```bash
docker build -t music-platform-api:stepb .
docker run --rm -d --name stepb-api-test -p 8000:8000 music-platform-api:stepb
```

Validation:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
curl -I http://127.0.0.1:8000/docs
docker logs stepb-api-test
docker stop stepb-api-test
```

Checkpoint:
- Image builds.
- Container starts without crashing.
- API and docs are reachable through mapped host port.

## Step C - Test container alone

Goal:
- Validate runtime behavior before introducing dependent services.

Recommended checks:

```bash
docker run --rm -d --name stepc-api-test -p 8000:8000 music-platform-api:stepb
docker inspect -f '{{.State.Running}}' stepc-api-test
docker inspect -f '{{.RestartCount}}' stepc-api-test
docker logs --tail 100 stepc-api-test
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/docs
docker stop stepc-api-test
```

Checkpoint:
- Running state remains `true`.
- Restart count remains `0`.
- Logs show normal startup and no traceback.

## Step D - Add Docker Compose (API + DB)

Goal:
- Run API and database as separate services managed together.

Compose must include:
- `api` service (FastAPI container).
- `db` service (PostgreSQL container).
- `DATABASE_URL` pointing from `api` to `db` service name.
- Service dependency/health strategy (`depends_on` + DB healthcheck).

Commands:

```bash
docker compose up -d --build
docker compose ps
```

Validation:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/songs/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Compose Song","artist":"Compose Tester"}'
curl http://127.0.0.1:8000/songs/
docker compose exec -T db psql -U postgres -d music_platform -c "SELECT COUNT(*) FROM songs;"
```

Checkpoint:
- Both services are running.
- API can read/write data with DB.
- Host-to-API mapping (`localhost:8000 -> api:8000`) works.

## Step E - Validate logs

Goal:
- Confirm there are no hidden startup, import, or DB connection errors.

Commands:

```bash
docker compose logs --tail=200 api
docker compose logs --tail=200 db
```

Expected API signals:
- `Started server process`
- `Waiting for application startup`
- `Application startup complete`
- `Uvicorn running on http://0.0.0.0:8000`

Expected DB signals:
- `database system is ready to accept connections`
- `listening on ... port 5432`

Red flags:
- `Traceback`
- `ModuleNotFoundError`
- `ImportError`
- `OperationalError`
- `connection refused`
- `could not connect`

Checkpoint:
- Startup and readiness logs are clean.
- No unresolved runtime or connectivity errors.

## Cleanup commands

```bash
docker compose down
docker compose down -v
```

Use `-v` to remove persisted DB volume and restart from a clean state.
