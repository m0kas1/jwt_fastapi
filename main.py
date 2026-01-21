from fastapi import Depends, FastAPI
from routers import authRouter
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from models.User import User
from models.Refresh import Token


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client = AsyncIOMotorClient(settings.DB_URL)

        # 2. Инициализируем Beanie
        # database_name - имя вашей базы данных
        await init_beanie(database=client.my_db_name, document_models=[User, Token])

        print("Startup: База данных подключена!")
        yield
        print("Shutdown: Отключение...")
    except:
        print('Сервер закрыл свою работу')


app = FastAPI(lifespan=lifespan)

app.include_router(
    authRouter.router,
    prefix="/api",
    tags=["api"],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}