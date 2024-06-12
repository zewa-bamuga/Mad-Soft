from app.domain.meme.core.repositories import MemeRepository
from app.domain.common import schemas

from loguru import logger


class MemeCreateCommand:
    def __init__(
            self,
            repository: MemeRepository,
    ):
        self.repository = repository

    async def __call__(self, payload: schemas.MemeCreate) -> None:
        meme_id_container = await self.repository.create_meme(
            schemas.MemeCreate(
                **payload.model_dump(),
            )
        )
        logger.info("Meme created: {meme_id}", meme_id=meme_id_container.id)
