"""create uuid v7 function

Revision ID: 6c3164c2dab9
Revises: 45ab151260cb
Create Date: 2025-12-04 15:33:37.430560

"""

from pathlib import Path
from typing import Sequence, Union

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c3164c2dab9"
down_revision: Union[str, Sequence[str], None] = "45ab151260cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


uuid_v7_functions = (
    Path(
        context.config.get_section_option(
            "extra",
            "functions.dir",
        )
    )
    / "uuid_v7"
)


def upgrade() -> None:
    op.execute(
        (uuid_v7_functions / "upgrade.sql").read_text(),
    )


def downgrade() -> None:
    op.execute(
        (uuid_v7_functions / "downgrade.sql").read_text(),
    )
