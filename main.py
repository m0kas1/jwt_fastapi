from routers import authRouter
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from exeptions.api_error import ApiError
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
    except Exception as e:
        print(e)

app = FastAPI(lifespan=lifespan)

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={
            "message": exc.message,
            "errors": exc.errors
        }
    )

app.include_router(
    authRouter.router,
    prefix="/api",
    tags=["api"],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Весь функциональ находится по пути /auth/!"}