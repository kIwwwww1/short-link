import uvicorn
import string
from secrets import choice
from fastapi import FastAPI


app = FastAPI()

ALPHABET: str = string.ascii_letters + string.digits

def genearate_random_slug() -> str:
    slug = ''
    for _ in range(6):
        slug += choice(ALPHABET)
    return slug

@app.post('/short_url')
async def generate_short_url(url: int): 
    return {'True': 'Ваша короткая ссылка'}

@app.get('/{slug}')
async def redirect_to_url(slug: str):
    return {'True': f'Ваша короткая ссылка {slug}'}




if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)