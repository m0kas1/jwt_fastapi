from fastapi import Request, Response, HTTPException, status
from models.User import User
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from config import settings
from validator import UserCreateRequest
from service.tokenservice import TokenService
from models.User import Roli_na_ruke
newToken = TokenService()

class authController:
    async def registration(self, user_data: UserCreateRequest):
            candidate = await User.find_one(User.username == user_data.username)
            if candidate:
                raise 'Такой пользователь уже есть'
            new_pass_hash = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(
                username =  user_data.username,
                password = new_pass_hash.decode('utf-8'),
                roles = [Roli_na_ruke(name_role="USER")]
            )
            await new_user.insert()
            rolki = [i.name_role for i in new_user.roles]
            data_user = {"id": str(new_user.id), "roles": rolki}
            token = newToken.generate_token(data_user)
            await newToken.save_refresh_token(new_user.id, token["refresh_token"])
            return {**token, "userId": data_user}
        # except Exception as e:

        #     return str(e)

    async def login(self, user_data: dict):
            candidate = await User.find_one(User.username == user_data['username'])
            if not candidate:
                raise HTTPException(status_code=400, detail="Неверные данные")
            valid = bcrypt.checkpw(user_data['password'].encode('utf-8'), candidate.password.encode('utf-8'))
            if not valid:
                raise HTTPException(status_code=400, detail="Неверные данные")

            rolki = [i.name_role for i in candidate.roles]

            token = newToken.generate_token({"id": str(candidate.id), "roles": rolki})
            return token

    async def getAll(self):
        users = await User.find().to_list()
        return users

    async def logout(self):
        return 1

    async def refresh(self):
        return 1