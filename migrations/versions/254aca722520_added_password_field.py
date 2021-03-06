"""added password field

Revision ID: 254aca722520
Revises: 97e98d738838
Create Date: 2022-05-09 16:28:13.382243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '254aca722520'
down_revision = '97e98d738838'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
