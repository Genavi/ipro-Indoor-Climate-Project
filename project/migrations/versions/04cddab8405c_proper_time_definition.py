"""proper time definition

Revision ID: 04cddab8405c
Revises: 75dc45a8afb7
Create Date: 2026-01-23 22:35:49.278118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '04cddab8405c'
down_revision: Union[str, Sequence[str], None] = '75dc45a8afb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Because I'm renaming a primary key column that is used by TimescaleDB
    # for partitioning, I need to drop the chunks first.
    op.execute("SELECT public.drop_chunks('sensor_readings', older_than => INTERVAL '0 seconds');")

    op.alter_column('sensor_readings', 'timestamp', new_column_name='time')

    # Recreating hypertable with new column name
    op.execute("SELECT create_hypertable('sensor_readings', 'time', if_not_exists => TRUE);")


def downgrade() -> None:
    """Downgrade schema."""
    # Because I'm renaming a primary key column that is used by TimescaleDB
    # for partitioning, I need to drop the chunks first.
    op.execute("SELECT public.drop_chunks('sensor_readings', older_than => INTERVAL '0 seconds');")

    op.alter_column('sensor_readings', 'time', new_column_name='timestamp')

    # Recreating hypertable with old column name
    op.execute("SELECT create_hypertable('sensor_readings', 'timestamp', if_not_exists => TRUE);")