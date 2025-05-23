"""add_identities_and_hourly_records

Revision ID: f9f37c6b5214
Revises: f503a5bf05a8
Create Date: 2025-05-14 20:58:35.662883

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f9f37c6b5214"
down_revision: Union[str, None] = "f503a5bf05a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "identities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("provider_user_id", sa.String(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=False),
        sa.Column("access_token", sa.String(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider", "provider_user_id", name="uq_user_provider_user_id"),
        sa.UniqueConstraint("user_id", "provider", name="uq_user_provider"),
    )

    op.create_table(
        "solar_panel_hourly_records",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("solar_panel_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("power_output_kw", sa.Float(), nullable=False),
        sa.Column("energy_generated_kwh", sa.Float(), nullable=False),
        sa.Column("predicted_power_output_kw", sa.Float(), nullable=True),
        sa.Column("efficiency_percent", sa.Float(), nullable=True),
        sa.Column("cell_temperature_celsius", sa.Float(), nullable=True),
        sa.Column("temperature_celsius", sa.Float(), nullable=True),
        sa.Column("irradiance", sa.Float(), nullable=True),
        sa.Column("poa_irradiance", sa.Float(), nullable=True),
        sa.Column("cloud_cover_percent", sa.Float(), nullable=True),
        sa.Column("wind_speed_kmh", sa.Float(), nullable=True),
        sa.Column("wind_direction_degrees", sa.Float(), nullable=True),
        sa.Column("humidity_percent", sa.Float(), nullable=True),
        sa.Column("precipitation_mm", sa.Float(), nullable=True),
        sa.Column("pressure_msl_hpa", sa.Float(), nullable=True),
        sa.Column("clear_sky_index", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["solar_panel_id"],
            ["solar_panels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("solar_panel_hourly_records")
    op.drop_table("identities")
    # ### end Alembic commands ###
