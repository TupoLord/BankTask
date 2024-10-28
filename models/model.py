from datetime import datetime
from sqlalchemy import MetaData, Table, Integer, String, TIMESTAMP, Column, Boolean, JSON, ForeignKey

metadata = MetaData()

bank = Table(
    "bank",
    metadata,
    Column("id", Integer, primary_key=True,),
    Column("bank_name", String, nullable=False),
)


role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

custom = Table(
    "custom",
    metadata,
    Column("id", Integer, primary_key=True,),
    Column("custom_name", String, nullable=False),
    Column("bank_name", String, nullable=False),
    Column("user_id", Integer, ForeignKey("user.id"))
)


# PEP 8




