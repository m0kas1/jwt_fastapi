class ApiError(Exception):
    def __init__(self, status, message, errors: list = None):
        super().__init__(message)

        self.status = status
        self.message = message
        self.errors = errors if errors is not None else []

    @classmethod
    def UnauthorizedError(cls):
        return ApiError(401, 'Пользователь не авторизован')

    @classmethod
    def BadRequestError(cls, message, error=[]):
        return ApiError(400, message, error)