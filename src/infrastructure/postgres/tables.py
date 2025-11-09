from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    UUID,
    JSON,
    DateTime)

metadata = MetaData()

dashboard_table = Table(
    "dashboard_table",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    ),
    Column("social", String, nullable=False),
    Column("company_id", Integer, nullable=False),
    Column("stats_kwargs", JSON, nullable=False),
    Column(
        "created_at",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
        ),
)

