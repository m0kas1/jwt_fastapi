from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import settings
from models.User import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def proverka_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt_de = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_key = jwt_de.get('id')
        if user_key is None:
            raise 'Плохо'
    except jwt.ExpiredSignatureError:
        return 0
    user_date = await User.get(user_key)
    if user_date is None:
        raise "Дела плохи"
    return user_date