"""postgres_init

Revision ID: 11f8eb503fb6
Revises: 
Create Date: 2023-08-16 17:15:24.926039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11f8eb503fb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('picture', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('token', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_table('subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user', sa.UUID(), nullable=False),
        sa.Column('subscriber', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['subscriber'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('videos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('file', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('user', sa.UUID(), nullable=False),
        sa.Column('like_count', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user'], ['users.id'], ondelete='restrict'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('videos_likes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('video', sa.Integer(), nullable=False),
        sa.Column('user', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['user'], ['users.id'], ),
        sa.ForeignKeyConstraint(['video'], ['videos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('videos_likes')
    op.drop_table('videos')
    op.drop_table('subscriptions')
    op.drop_table('refresh_tokens')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
