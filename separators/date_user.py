from service.tokenservice import TokenService

newToken = TokenService()

class SeparatorPayload:

    @staticmethod
    async def get_payload(user_id: str, roles: list[str]):
        data_user_to_dict = {"id": user_id, "roles": roles}
        token = newToken.generate_token(data_user_to_dict)
        await newToken.save_refresh_token(user_id, token["refresh_token"])
        return {**token, "userId": data_user_to_dict}