from fastapi import Request, Response
from validator import ValidUserDates
from service.tokenservice import TokenService
from service.userservice import UserService

newToken = TokenService()
userService = UserService()

class authController:
    async def registration(self, user_data: ValidUserDates, res: Response):
        register = await userService.registration(user_data)
        res.set_cookie(
            key="refresh_token",
            value=register["refresh_token"],
            httponly=True,
            samesite="lax",
            secure=True,  # Ставь False, если тестируешь на localhost без https
            max_age=30 * 24 * 60 * 60
        )
        return register

    async def login(self, user_data: ValidUserDates, res: Response):
        user_data_on_token = await userService.login(user_data)
        res.set_cookie(
            key="refresh_token",
            value=user_data_on_token["refresh_token"],
            httponly=True,
            samesite="lax",
            secure=True,  # Ставь False, если тестируешь на localhost без https
            max_age=30 * 24 * 60 * 60
        )
        return {"message": "Успешная аутентификация"}

    async def logout(self, res: Response, req: Request):
        read_refresh_cookie = req.cookies.get('refresh_token')
        await userService.logout(read_refresh_cookie)
        res.delete_cookie('refresh_token')
        return {"message": "Успешный выход"}

    async def getAll(self):
        return userService.getAll()

    async def refresh(self, res: Response, req: Request):
        read_refresh_cookie = req.cookies.get('refresh_token')
        user_data_on_token = await userService.refresh(read_refresh_cookie)
        res.delete_cookie('refresh_token')
        res.set_cookie(
            key="refresh_token",
            value=user_data_on_token["refresh_token"],
            httponly=True,
            samesite="lax",
            secure=True,  # Ставь False, если тестируешь на localhost без https
            max_age=30 * 24 * 60 * 60
        )
        return {"message": "Успешное обновление токена"}