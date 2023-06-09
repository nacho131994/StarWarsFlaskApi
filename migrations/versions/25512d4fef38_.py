"""empty message

Revision ID: 25512d4fef38
Revises: 082a8cf72084
Create Date: 2023-05-16 17:45:26.775740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25512d4fef38'
down_revision = '082a8cf72084'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('target', sa.String(length=80), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jwt_token_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jwt_token', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('mass', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('climate', sa.String(length=120), nullable=False),
    sa.Column('gravity', sa.String(length=120), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planet')
    op.drop_table('person')
    op.drop_table('jwt_token_blocklist')
    op.drop_table('favorite')
    # ### end Alembic commands ###
