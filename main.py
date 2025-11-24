import uvicorn
from contextlib import asynccontextmanager
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Body, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from database.db import engine, new_session
from database.models import Base
from exceptions import NoLongUrlFoundError, SlugAlreadyExistsError
from service import create_short_url, get_url_by_slug

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

async def get_session():
    async with new_session() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_session)]


@app.post('/short_url')
async def generate_short_url(session: session_dep, long_url: str = Body(embed=True)): 
    try:
        new_slug = await create_short_url(long_url, session)
    except SlugAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='что то пошло не так')
    return {'data': new_slug}       

@app.get('/{slug}')
async def redirect_to_url(slug: str, session: session_dep):
    try:
        long_url = await get_url_by_slug(slug, session)
    except NoLongUrlFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ссылка не существует')
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)




if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)