import enum
from uuid import UUID

from a8t_tools.schemas.pydantic import APIModel


class Meme(APIModel):
    id: UUID
    meme_attachment_id: str
    avatar_attachment: str


# class MemeCreate(APIModel):
#     avatar_attachment_id: UUID | None = None


class MemeSorts(enum.StrEnum):
    id = enum.auto()
