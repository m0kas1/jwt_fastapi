import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from models.Refresh import Token
class TokenService:
    def generate_token(self, payload: dict):
        access_token = self._create_token(
            payload,
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            settings.JWT_ACCESS_SECRET_KEY
        )

        refresh_token = self._create_token(
            payload,
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            settings.JWT_REFRESH_SECRET_KEY
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    async def save_refresh_token(self, id_user_date, refresh_token):
        candidate = await Token.find_one(Token.id_user == id_user_date)
        if candidate:
            candidate.refresh_token = refresh_token
            await candidate.save()
            return {'message': "Обновлено"}

        new_reg = Token(id_user=id_user_date,
                        refresh_token=refresh_token)
        await new_reg.insert()
        return {'message': "Успех"}

    async def removeToken(self, refreshToken):
        token_data = await Token.find_one(Token.refresh_token == refreshToken).delete()
        return token_data

    def validateAccessToken(self, token):
        try:
            user_data = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM])
            return user_data
        except:
            return None

    def validateRefreshToken(self, token):
        try:
            user_data = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
            return user_data
        except:
            return None

    async def findToken(self, refreshToken):
        token_data = await Token.find_one(Token.refresh_token == refreshToken)
        return token_data

    def _create_token(self, payload: dict, expires_delta: timedelta, secret_key: str) -> str:
        """Вспомогательный метод для создания JWT"""
        to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            secret_key,
            algorithm=settings.ALGORITHM
        )