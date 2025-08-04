"""add timezone

Revision ID: 21334e790b3f
Revises: 6f2fd6a5d48b
Create Date: 2025-08-05 20:29:29.942152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '21334e790b3f'
down_revision: Union[str, None] = '6f2fd6a5d48b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Identities
    op.execute("""
        ALTER TABLE identities
        ALTER COLUMN expires_at TYPE TIMESTAMP WITH TIME ZONE
        USING expires_at AT TIME ZONE 'UTC';
    """)
    op.execute("""
        ALTER TABLE identities
        ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at SET NOT NULL;
    """)
    op.execute("""
        ALTER TABLE identities
        ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at SET NOT NULL;
    """)

    # Inverters
    op.execute("""
        ALTER TABLE inverters
        ALTER COLUMN installation_date TYPE TIMESTAMP WITH TIME ZONE
        USING installation_date AT TIME ZONE 'UTC',
        ALTER COLUMN installation_date SET NOT NULL;
    """)
    op.execute("""
        ALTER TABLE inverters
        ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at SET NOT NULL;
    """)
    op.execute("""
        ALTER TABLE inverters
        ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at SET NOT NULL;
    """)

    # solar_panel_hourly_records
    op.execute("""
        ALTER TABLE solar_panel_hourly_records
        ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at SET NOT NULL;
    """)
    op.execute("""
        ALTER TABLE solar_panel_hourly_records
        ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at SET NOT NULL;
    """)

    # solar_panels
    op.execute("""
        ALTER TABLE solar_panels
        ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at SET NOT NULL;
    """)
    op.execute("""
        ALTER TABLE solar_panels
        ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at SET NOT NULL;
    """)

    # users
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at SET NOT NULL;
    """)
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at SET NOT NULL;
    """)


def downgrade() -> None:
    # Identities
    op.execute("""
        ALTER TABLE identities
        ALTER COLUMN expires_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING expires_at AT TIME ZONE 'UTC';
    """)
    op.execute("""
        ALTER TABLE identities
        ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at DROP NOT NULL;
    """)
    op.execute("""
        ALTER TABLE identities
        ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at DROP NOT NULL;
    """)

    # Inverters
    op.execute("""
        ALTER TABLE inverters
        ALTER COLUMN installation_date TYPE TIMESTAMP WITHOUT TIME ZONE
        USING installation_date AT TIME ZONE 'UTC',
        ALTER COLUMN installation_date SET NOT NULL;
    """)
    op.execute("""
        ALTER TABLE inverters
        ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at DROP NOT NULL;
    """)
    op.execute("""
        ALTER TABLE inverters
        ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at DROP NOT NULL;
    """)

    # solar_panel_hourly_records
    op.execute("""
        ALTER TABLE solar_panel_hourly_records
        ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at DROP NOT NULL;
    """)
    op.execute("""
        ALTER TABLE solar_panel_hourly_records
        ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at DROP NOT NULL;
    """)

    # solar_panels
    op.execute("""
        ALTER TABLE solar_panels
        ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at DROP NOT NULL;
    """)
    op.execute("""
        ALTER TABLE solar_panels
        ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at DROP NOT NULL;
    """)

    # users
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING created_at AT TIME ZONE 'UTC',
        ALTER COLUMN created_at DROP NOT NULL;
    """)
    op.execute("""
        ALTER TABLE users
        ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE
        USING updated_at AT TIME ZONE 'UTC',
        ALTER COLUMN updated_at DROP NOT NULL;
    """)
