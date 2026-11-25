class UserNotFoundError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class InvalidAccessTokenError(Exception):
    pass