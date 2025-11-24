from fastapi import status
from random_slug import genearate_random_slug
from database.crud import add_slug_to_database, get_url_by_slug_on_database

async def create_short_url(long_url: str) -> str:
    slug = genearate_random_slug()
    await add_slug_to_database(slug=slug, long_url=long_url)
    return slug


async def get_url_by_slug(slug: str) -> str | None:
    long_url = await get_url_by_slug_on_database(slug)
    if not long_url:
        status.HTTP_404_NOT_FOUND
    return long_url



