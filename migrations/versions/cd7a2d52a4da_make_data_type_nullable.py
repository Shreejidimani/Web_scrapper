"""Make data_type nullable

Revision ID: cd7a2d52a4da
Revises: 
Create Date: 2025-02-14 15:16:31.145499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd7a2d52a4da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scraping_history', schema=None) as batch_op:
        batch_op.alter_column('data_type',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scraping_history', schema=None) as batch_op:
        batch_op.alter_column('data_type',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###
