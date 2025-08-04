"""add server default to inverter table

Revision ID: a9e342d12e89
Revises: 21334e790b3f
Create Date: 2025-08-05 20:52:06.243924
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a9e342d12e89'
down_revision: Union[str, None] = '21334e790b3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Set default for created_at
    op.alter_column(
        'inverters',
        'created_at',
        server_default=sa.text('CURRENT_TIMESTAMP'),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )

    # Set default for updated_at (insert)
    op.alter_column(
        'inverters',
        'updated_at',
        server_default=sa.text('CURRENT_TIMESTAMP'),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )

    # Add ON UPDATE trigger for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    op.execute("""
        CREATE TRIGGER set_updated_at
        BEFORE UPDATE ON inverters
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
    """)


def downgrade() -> None:
    # Remove trigger and function
    op.execute("DROP TRIGGER IF EXISTS set_updated_at ON inverters;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column;")

    # Remove server defaults
    op.alter_column(
        'inverters',
        'updated_at',
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )

    op.alter_column(
        'inverters',
        'created_at',
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )
