import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.post('/short_url')
async def generate_short_url(url: int): 
    return {'True': 'Ваша короткая ссылка'}

@app.get('/{slug}')
async def redirect_to_url(slug: str):
    return {'True': f'Ваша короткая ссылка {slug}'}




if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)