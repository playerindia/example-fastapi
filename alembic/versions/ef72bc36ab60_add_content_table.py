"""add content table

Revision ID: ef72bc36ab60
Revises: a2f7a71a7426
Create Date: 2024-07-10 20:47:25.949108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef72bc36ab60'
down_revision: Union[str, None] = 'a2f7a71a7426'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
      op.add_column('posts',sa.Column('content',sa.String(),nullable=False)
                    )
      pass


def downgrade():
    op.drop_column('posts','content')
    pass
