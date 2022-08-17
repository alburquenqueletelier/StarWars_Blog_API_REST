"""empty message

Revision ID: f5823f3eae56
Revises: f5de1bf230f9
Create Date: 2022-08-17 01:05:11.265324

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f5823f3eae56'
down_revision = 'f5de1bf230f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('film_ibfk_1', 'film', type_='foreignkey')
    op.drop_column('film', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('film', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('film_ibfk_1', 'film', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###