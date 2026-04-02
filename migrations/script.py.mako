"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
from __future__ import annotations

import sqlalchemy as sa
from typing import Any, cast

from alembic import op as alembic_operations
${imports if imports else ""}

op = cast(Any, alembic_operations)

# revision identifiers, used by Alembic.
REVISION = ${repr(up_revision)}
DOWN_REVISION = ${repr(down_revision)}
BRANCH_LABELS = ${repr(branch_labels)}
DEPENDS_ON = ${repr(depends_on)}

globals()["revision"] = REVISION
globals()["down_revision"] = DOWN_REVISION
globals()["branch_labels"] = BRANCH_LABELS
globals()["depends_on"] = DEPENDS_ON


def upgrade() -> None:
    """Apply the schema changes for this revision."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Revert the schema changes for this revision."""
    ${downgrades if downgrades else "pass"}
