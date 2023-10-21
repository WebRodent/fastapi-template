"""Add a User Table

Revision ID: 922a278f54bc
Revises: 53e4881be978
Create Date: 2023-10-21 21:07:36.814268

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "922a278f54bc"
down_revision: Union[str, None] = "53e4881be978"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, index=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("auth_method", sa.String),
    )


def downgrade() -> None:
    op.drop_table("users")
