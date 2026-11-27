
class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidAccessTokenError(Exception):
    pass


class InvalidUserDataError(Exception):
    pass


# Notification exceptions

class NotificationError(Exception):
    pass


class NotificationNotFoundError(NotificationError):
    pass


class InvalidRecipientError(NotificationError):
    pass


class InvalidNotificationContentError(NotificationError):
    pass


class UnsupportedChannelError(NotificationError):
    pass
