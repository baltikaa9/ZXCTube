"""video_preview

Revision ID: 8daeb228da52
Revises: 11f8eb503fb6
Create Date: 2023-08-16 17:54:58.556803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8daeb228da52'
down_revision = '11f8eb503fb6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('preview', sa.String(), nullable=True))
    op.drop_constraint('videos_user_fkey', 'videos', type_='foreignkey')
    op.create_foreign_key(None, 'videos', 'users', ['user'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'videos', type_='foreignkey')
    op.create_foreign_key('videos_user_fkey', 'videos', 'users', ['user'], ['id'], ondelete='RESTRICT')
    op.drop_column('videos', 'preview')
    # ### end Alembic commands ###
