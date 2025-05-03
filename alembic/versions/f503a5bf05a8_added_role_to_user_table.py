"""Added role to user table

Revision ID: f503a5bf05a8
Revises: cef4b7c5f22f
Create Date: 2025-02-21 21:39:32.020203

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f503a5bf05a8"
down_revision: Union[str, None] = "cef4b7c5f22f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the ENUM type first
    role_enum = sa.Enum("ADMIN", "USER", name="roles")
    role_enum.create(op.get_bind())  # Explicitly create the type in PostgreSQL

    # Add the role column using the ENUM type
    op.add_column(
        "users", sa.Column("role", role_enum, nullable=False, server_default="USER")
    )


def downgrade() -> None:
    # Drop the role column first
    op.drop_column("users", "role")

    # Drop the ENUM type (only if no other table is using it)
    op.execute("DROP TYPE roles")
