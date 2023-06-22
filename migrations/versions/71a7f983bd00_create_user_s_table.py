"""Create User's table 

Revision ID: 71a7f983bd00
Revises: 
Create Date: 2023-06-21 16:58:54.489871

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "71a7f983bd00"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Users",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("salary", sa.Float(), nullable=False),
        sa.Column("next_salary_up", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Users")
    # ### end Alembic commands ###
