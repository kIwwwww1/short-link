from sqlalchemy import select
from database.models import ShortURL
from database.db import new_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import SlugAlreadyExistsError

async def add_slug_to_database(slug: str, long_url: str, session: AsyncSession):
    new_slug = ShortURL(
        slug=slug,
        long_url=long_url
        )
    session.add(new_slug)
    try:
        await session.commit()
    except IntegrityError:
        raise SlugAlreadyExistsError

async def get_url_by_slug_on_database(slug: str, session: AsyncSession) -> str | None:
    query = select(ShortURL).filter_by(slug=slug)
    result: ShortURL | None = (await session.execute(query)).scalar_one_or_none()
    return result.long_url if result.long_url else None
    
        

