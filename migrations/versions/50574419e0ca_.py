"""empty message

Revision ID: 50574419e0ca
Revises: 06e44712f417
Create Date: 2022-08-16 19:26:41.457423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '50574419e0ca'
down_revision = '06e44712f417'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('episode_id', sa.Integer(), nullable=False),
    sa.Column('director', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=True),
    sa.Column('cost_in_credits', sa.String(length=50), nullable=True),
    sa.Column('vehicle_class', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('hair_color', sa.String(length=50), nullable=True),
    sa.Column('birth_year', sa.String(length=10), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('homeworld_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['homeworld_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('film_planet',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('film_id', 'planet_id')
    )
    op.create_table('film_vehicle',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('film_id', 'vehicle_id')
    )
    op.create_table('character_vehicle',
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('character_id', 'vehicle_id')
    )
    op.create_table('film_character',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.PrimaryKeyConstraint('film_id', 'character_id')
    )
    op.add_column('user', sa.Column('username', sa.String(length=50), nullable=False))
    op.drop_column('user', 'is_active')
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=80), nullable=False))
    op.add_column('user', sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('user', 'username')
    op.drop_table('film_character')
    op.drop_table('character_vehicle')
    op.drop_table('film_vehicle')
    op.drop_table('film_planet')
    op.drop_table('character')
    op.drop_table('vehicle')
    op.drop_table('planet')
    op.drop_table('film')
    # ### end Alembic commands ###
