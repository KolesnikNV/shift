"""Change User's model

Revision ID: 02c109794eb9
Revises: 8bdead7a445e
Create Date: 2023-06-22 19:49:27.618131

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '02c109794eb9'
down_revision = '8bdead7a445e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.drop_column('Users', 'roles')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('roles', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=False))
    op.drop_column('Users', 'is_admin')
    # ### end Alembic commands ###