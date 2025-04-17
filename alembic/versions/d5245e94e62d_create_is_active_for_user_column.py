"""Create is_active for user column

Revision ID: d5245e94e62d
Revises: 
Create Date: 2025-04-17 12:30:16.341510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'd5245e94e62d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""Upgrade schema."""
def upgrade():
    conn = op.get_bind()
    inspector = inspect(conn)

    columns = [col["name"] for col in inspector.get_columns("users")]
    if "is_active" not in columns:
        op.add_column("users", sa.Column("is_active", sa.Boolean(), server_default=sa.sql.expression.true()))


"""Downgrade schema."""
def downgrade() -> None:
    # Drop the 'is_active' column
    op.drop_column('users', 'is_active')
