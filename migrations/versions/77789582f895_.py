"""empty message

Revision ID: 77789582f895
Revises: 
Create Date: 2021-01-11 14:09:24.515953

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '77789582f895'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='users')
    op.drop_index('mobile', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=220), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=220), nullable=False),
    sa.Column('mobile', mysql.VARCHAR(length=15), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('createdAt', mysql.DATETIME(), nullable=True),
    sa.Column('updatedAt', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('mobile', 'users', ['mobile'], unique=True)
    op.create_index('email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###
