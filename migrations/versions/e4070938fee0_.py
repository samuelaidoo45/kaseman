"""empty message

Revision ID: e4070938fee0
Revises: 
Create Date: 2023-11-26 11:53:57.801448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4070938fee0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loan_classification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('loan_classification_name', sa.String(length=100), nullable=False),
    sa.Column('loan_classification_desc', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loan_classification_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('branch_name', sa.String(length=100), nullable=False),
    sa.Column('loan_class_id', sa.String(length=100), nullable=True),
    sa.Column('filename', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loan_classification_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('loan_class_file_id', sa.String(length=100), nullable=False),
    sa.Column('arrangement', sa.String(length=100), nullable=True),
    sa.Column('application_id', sa.String(length=100), nullable=True),
    sa.Column('company_branch', sa.String(length=100), nullable=True),
    sa.Column('account', sa.String(length=100), nullable=True),
    sa.Column('officer', sa.String(length=100), nullable=True),
    sa.Column('product_name', sa.String(length=100), nullable=True),
    sa.Column('customer', sa.String(length=100), nullable=True),
    sa.Column('customer_name', sa.String(length=100), nullable=True),
    sa.Column('opening_date', sa.String(length=100), nullable=True),
    sa.Column('first_pay_date', sa.String(length=100), nullable=True),
    sa.Column('maturity_date', sa.String(length=100), nullable=True),
    sa.Column('term', sa.String(length=100), nullable=True),
    sa.Column('interest_rate', sa.String(length=100), nullable=True),
    sa.Column('ccy', sa.String(length=100), nullable=True),
    sa.Column('commitment', sa.String(length=100), nullable=True),
    sa.Column('principal', sa.String(length=100), nullable=True),
    sa.Column('due_date', sa.String(length=100), nullable=True),
    sa.Column('overdue', sa.String(length=100), nullable=True),
    sa.Column('resch_id', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loan_classification_items')
    op.drop_table('loan_classification_files')
    op.drop_table('loan_classification')
    # ### end Alembic commands ###