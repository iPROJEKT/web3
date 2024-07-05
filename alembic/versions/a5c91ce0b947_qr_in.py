"""QR in

Revision ID: a5c91ce0b947
Revises: 34b056da2e43
Create Date: 2024-07-04 20:51:15.431589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5c91ce0b947'
down_revision: Union[str, None] = '34b056da2e43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('qr_code', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'qr_code')
    # ### end Alembic commands ###