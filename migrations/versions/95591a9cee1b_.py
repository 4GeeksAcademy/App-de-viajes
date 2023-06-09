"""empty message

Revision ID: 95591a9cee1b
Revises: 4b979f5e7b0a
Create Date: 2023-06-09 23:03:35.063282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95591a9cee1b'
down_revision = '4b979f5e7b0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
