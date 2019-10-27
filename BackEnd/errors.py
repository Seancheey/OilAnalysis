class BackEndError(Exception):
    pass


class UserAlreadyExistsError(BackEndError):
    pass


class EmailAlreadyExistsError(BackEndError):
    pass


class UserDoNotExistsError(BackEndError):
    pass


class UserPasswordNoMatchError(BackEndError):
    pass


class LoginSessionExpired(BackEndError):
    pass
