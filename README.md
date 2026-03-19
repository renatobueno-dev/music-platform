# Checkpoint Level 3 - Stage 1

Minimal FastAPI + SQLAlchemy structure for a music platform domain.

## Scope defined

- `Song` resource
- `Playlist` resource
- Many-to-many relationship through `playlist_songs`

See [DOMAIN_SCOPE.md](./DOMAIN_SCOPE.md) for detailed fields and relationship decisions.

## Project structure

```text
.
├── .gitignore
├── DOMAIN_SCOPE.md
├── README.md
├── requirements.txt
└── app
    ├── __init__.py
    ├── database.py
    ├── main.py
    ├── models
    │   ├── __init__.py
    │   ├── base.py
    │   ├── playlist.py
    │   ├── playlist_song.py
    │   └── song.py
    ├── routes
    │   ├── __init__.py
    │   ├── health.py
    │   ├── playlists.py
    │   └── songs.py
    ├── schemas
    │   ├── __init__.py
    │   ├── playlist.py
    │   └── song.py
    └── services
        ├── __init__.py
        ├── playlist_service.py
        └── song_service.py
```

### What each part does

| Path | Responsibility |
| --- | --- |
| `DOMAIN_SCOPE.md` | Defines the domain model and relationship decisions for `Song` and `Playlist`. |
| `requirements.txt` | Lists runtime dependencies (`fastapi`, `uvicorn`, `sqlalchemy`). |
| `app/main.py` | API entry point, application creation, router registration, and startup table creation. |
| `app/database.py` | SQLAlchemy engine/session setup and FastAPI dependency provider (`get_session`). |
| `app/models/base.py` | Shared SQLAlchemy declarative base class. |
| `app/models/song.py` | `Song` ORM model and relationship to playlists. |
| `app/models/playlist.py` | `Playlist` ORM model and relationship to songs. |
| `app/models/playlist_song.py` | Association table model for the many-to-many relation and `added_at` metadata. |
| `app/schemas/song.py` | Pydantic request/response schemas for song payload validation and serialization. |
| `app/schemas/playlist.py` | Pydantic request/response schemas for playlist payload validation and serialization. |
| `app/routes/health.py` | Healthcheck endpoint for service status. |
| `app/routes/songs.py` | HTTP endpoints for listing and creating songs. |
| `app/routes/playlists.py` | HTTP endpoints for listing and creating playlists. |
| `app/services/song_service.py` | Database operations used by song routes (list/create). |
| `app/services/playlist_service.py` | Database operations used by playlist routes (list/create). |

### Layer flow

Request flow follows this order:

1. `routes/*` receives and validates HTTP input.
2. `schemas/*` enforces input/output contracts.
3. `services/*` executes business/database operations.
4. `models/*` maps Python objects to database tables.
5. `database.py` manages sessions used across route handlers.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the API:

```bash
uvicorn app.main:app --reload
```

4. Open docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Initial endpoints

- `GET /`
- `GET /health`
- `GET /songs/`
- `POST /songs/`
- `GET /playlists/`
- `POST /playlists/`
