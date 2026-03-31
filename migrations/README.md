# Alembic Migrations

This directory is the migration home for schema history.

Operational workflow source of truth: [docs/MIGRATIONS.md](../docs/MIGRATIONS.md).

## Structure

- `env.py`: Alembic runtime environment wired to `app.models.Base.metadata`
- `script.py.mako`: migration revision template
- `versions/`: migration revision files

## Conventions

- `DATABASE_URL` is required when running Alembic commands.
- Autogenerate must be based on SQLAlchemy models and reviewed before apply.
- After baseline adoption, schema changes must be migration-backed.

Create a new revision when model changes affect persisted schema:

- tables, columns, indexes, constraints, defaults, nullability, or foreign keys

## Example commands

```bash
DATABASE_URL=sqlite:///./music.db ./.venv/bin/alembic revision --autogenerate -m "describe change"
DATABASE_URL=sqlite:///./music.db ./.venv/bin/alembic upgrade head
DATABASE_URL=sqlite:///./music.db ./.venv/bin/alembic downgrade -1
```

## Current baseline

- Baseline revision: `abff2336451a`
- Description: `baseline schema`

If a database was created before migration adoption and already matches baseline schema, stamp once:

```bash
DATABASE_URL=<your-db-url> ./.venv/bin/alembic stamp abff2336451a
DATABASE_URL=<your-db-url> ./.venv/bin/alembic upgrade head
```
