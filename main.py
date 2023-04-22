from authentication import authentication
from database.database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from model import models
from routers import user_routes, post_routes, comment_routes
from seeder import data_generator

app = FastAPI()


@app.get("/")
async def root():
    return "Hello world!"


app.include_router(user_routes.router)
app.include_router(authentication.router)
app.include_router(post_routes.router)
app.include_router(comment_routes.router)
app.include_router(data_generator.router)

origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')
