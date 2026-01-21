import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from models.Refresh import Token
class TokenService:
    def generate_token(self, payload: dict):
        to_encode_access = payload.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode_access.update({"exp": expire})
        print(to_encode_access)
        encoded_access_jwt = jwt.encode(to_encode_access, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM)
        to_encode_refresh = payload.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode_refresh.update({"exp": expire})
        print(to_encode_refresh)
        encoded_refresh_jwt = jwt.encode(to_encode_refresh, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
        return {"access_token": encoded_access_jwt, "refresh_token": encoded_refresh_jwt}

    async def save_refresh_token(self, id_userok, refresh_token):
        candidate = await Token.find_one(Token.id_user == id_userok)
        if candidate:
            candidate.refresh_token = refresh_token
            return candidate.save()

        new_reg = Token(id_user=id_userok,
                        refresh_token=refresh_token)
        await new_reg.insert()
        return {'message': "Успех"}
# try:
#     jwt.decode(token, "secret", algorithms=["HS256"])
# except jwt.ExpiredSignatureError:
#     print("expired")