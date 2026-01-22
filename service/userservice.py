from models.User import User
import bcrypt
from validator import ValidUserDates
from service.tokenservice import TokenService
from models.User import Roli_na_ruke
from exeptions.api_error import ApiError

newToken = TokenService()

class UserService:
    async def registration(self, user_date: ValidUserDates):
        candidate = await User.find_one(User.username == user_date.username)

        if candidate:
            raise ApiError.BadRequestError("Пользователь уже существует")

        pass_hash = bcrypt.hashpw(user_date.password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(
            username=user_date.username,
            password=pass_hash.decode('utf-8'),
            roles=[Roli_na_ruke(name_role="USER")]
        )
        await new_user.insert()

        roles_to_string = [role_obj.name_role for role_obj in new_user.roles]
        data_user_to_dict = {"id": str(new_user.id), "roles": roles_to_string}
        token = newToken.generate_token(data_user_to_dict)
        await newToken.save_refresh_token(new_user.id, token["refresh_token"])
        return {**token, "userId": data_user_to_dict}

    async def login(self, user_date: ValidUserDates):
        candidate = await User.find_one(User.username == user_date.username)

        if not candidate:
            raise ApiError.BadRequestError("Неверные данные")
        pass_verif = bcrypt.checkpw(user_date.password.encode('utf-8'), candidate.password.encode('utf-8'))
        if not pass_verif:
            raise ApiError.BadRequestError("Неверный пароль")

        roles_to_string = [role_obj.name_role for role_obj in candidate.roles]
        data_user_to_dict = {"id": str(candidate.id), "roles": roles_to_string}
        token = newToken.generate_token(data_user_to_dict)
        await newToken.save_refresh_token(candidate.id, token["refresh_token"])
        return {**token, "userId": data_user_to_dict}

    async def logout(self, refresh_token):
        token = await newToken.removeToken(refresh_token)
        return token

    async def refresh(self, refresh_token):
        if not refresh_token:
            raise ApiError.UnauthorizedError()

        userData = newToken.validateRefreshToken(refresh_token)
        tokenFromDB = await newToken.findToken(refresh_token)

        if not userData or not tokenFromDB:
            raise ApiError.UnauthorizedError()

        roles = [role for role in userData['roles']]
        data_user_to_dict = {"id": str(userData['id']), "roles": roles}
        token = newToken.generate_token(data_user_to_dict)
        await newToken.save_refresh_token(userData['id'], token["refresh_token"])
        return {**token, "userId": data_user_to_dict}

    async def getAll(self):
        users = await User.find().to_list()
        return users