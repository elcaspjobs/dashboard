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
    DateTime,
    BigInteger, ForeignKey, Boolean, Text)

metadata = MetaData()

publication_table = Table(
    "feed_publications",
    metadata,
    Column("id", BigInteger, primary_key=True, unique=True),
    Column("feed_id", BigInteger, ForeignKey("user_neuronnewsmodel.id"), nullable=False),
    Column("connection_id", BigInteger, ForeignKey("user_connections.id"), nullable=False),
    Column("publish_time", DateTime(timezone=True), nullable=True),
    Column("result_url", String(500), nullable=True),
)

feed_table = Table(
    "user_neuronnewsmodel",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("company_id", Integer, nullable=True),
)


connection_table = Table(
    "user_connections",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("social", String(255), nullable=False),
    Column("name", String(255), nullable=True),
    Column("token_status", Boolean, default=False),
    Column("account_id", Text, nullable=True),
    Column("oauth_token", Text, nullable=True),
    Column("access_token", String(300), nullable=True),
    Column("client_secret", Text, nullable=True),
    Column("refresh_token", Text, nullable=True),
    Column("linkedin_org", Boolean, default=False),
)

dashboard = Table(
    "dashboard",
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
    Column("statistic", JSON, nullable=False),
    Column(
        "created_at",
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    ),
)
