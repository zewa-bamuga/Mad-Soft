import uuid
from typing import List
from uuid import UUID

from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from pydantic import BaseModel
from sqlalchemy import ColumnElement, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models, enums
from app.domain.common.schemas import IdContainer
from app.domain.meme.core import schemas
from app.domain.common import schemas as meme


class MemeRepository(CrudRepositoryMixin[models.Meme]):
    load_options: list[ExecutableOption] = [
        selectinload(models.Meme.avatar_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Meme
        self.transaction = transaction

    async def get_memes(
            self,
            pagination: PaginationCallable[schemas.Meme] | None = None,
            sorting: SortingData[schemas.MemeSorts] | None = None,
    ) -> Paginated[schemas.Meme]:
        return await self._get_list(
            schemas.Meme,
            pagination=pagination,
            sorting=sorting,
            options=self.load_options,
        )

    async def create_meme(self, payload: meme.MemeCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def delete_meme(self, meme_id: UUID) -> None:
        return await self._delete(meme_id)
