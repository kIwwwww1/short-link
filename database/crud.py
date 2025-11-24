from sqlalchemy import select
from database.models import ShortURL
from database.db import new_session

async def add_slug_to_database(slug: str, long_url: str):
    async with new_session() as session:
        new_slug = ShortURL(
            slug=slug,
            long_url=long_url
            )
        session.add(new_slug)
        await session.commit()

async def get_url_by_slug_on_database(slug: str) -> str | None:
    async with new_session() as session:
        query = select(ShortURL).filter_by(slug=slug)
        result: ShortURL | None = (await session.execute(query)).scalar_one_or_none()
        return result.long_url if result.long_url else None
    
        

