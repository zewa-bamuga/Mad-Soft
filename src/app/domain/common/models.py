import datetime
import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


@orm.as_declarative()
class Base:
    __tablename__: str

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Attachment(Base):
    __tablename__ = "attachment"

    name: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    path: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    uri: orm.Mapped[Optional[str]] = orm.mapped_column(String, nullable=True)


class Meme(Base):
    __tablename__ = "meme"

    avatar_attachment_id = orm.mapped_column(
        UUID(as_uuid=True),
        ForeignKey("attachment.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    avatar_attachment = relationship(
        "Attachment",
        backref="user_avatar_attachment",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )

    description: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
