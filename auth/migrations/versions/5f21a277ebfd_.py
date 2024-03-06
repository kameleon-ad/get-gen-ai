"""

Revision ID: 5f21a277ebfd
Revises: 
Create Date: 2024-03-06 17:51:41.051243

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5f21a277ebfd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('user_identity', sa.String(length=50), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('expires', mysql.INTEGER(unsigned=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('created_date', mysql.INTEGER(unsigned=True), nullable=True),
    sa.Column('modified_date', mysql.INTEGER(unsigned=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_created_date'), ['created_date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_created_date'))

    op.drop_table('user')
    op.drop_table('token')
    # ### end Alembic commands ###