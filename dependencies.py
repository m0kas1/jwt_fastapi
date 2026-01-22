from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
from config import settings
from models.User import User
from exeptions.api_error import ApiError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def proverka_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt_de = jwt.decode(token,
                            settings.JWT_ACCESS_SECRET_KEY,
                            settings.ALGORITHM)

        user_key = jwt_de.get('id')

        if user_key is None:
            raise ApiError.BadRequestError("Не удалось подтвердить учетные данные")
    except ExpiredSignatureError:
        raise ApiError.BadRequestError("Срок действия JWT иссек")
    except InvalidTokenError:
        raise ApiError.BadRequestError("Токен поддельный или битый")
    except Exception as e:
        return str(e)

    user_date = await User.get(user_key)
    if user_date is None:
        raise ApiError.BadRequestError("Ошибка данных")

    return user_date