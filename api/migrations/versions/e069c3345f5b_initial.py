"""Initial

Revision ID: e069c3345f5b
Revises: 
Create Date: 2025-02-06 01:08:00.448132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e069c3345f5b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hits',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ts', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hits')
    # ### end Alembic commands ###
