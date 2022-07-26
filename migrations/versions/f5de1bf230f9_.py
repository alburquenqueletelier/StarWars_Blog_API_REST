"""empty message

Revision ID: f5de1bf230f9
Revises: 718745742640
Create Date: 2022-08-17 01:03:39.985575

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f5de1bf230f9'
down_revision = '718745742640'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('film', 'director',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('film', 'director',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###
