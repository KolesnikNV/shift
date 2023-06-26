"""Change User's model

Revision ID: 8bdead7a445e
Revises: 99aa00eaa09d
Create Date: 2023-06-22 19:45:16.211358

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8bdead7a445e'
down_revision = '99aa00eaa09d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('roles', postgresql.ARRAY(sa.String()), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'roles')
    # ### end Alembic commands ###
