from sqlalchemy import Column
from abc import *
from BackEnd.objects import *


class BackEndError(Exception, ABC):
    """Error superclass for all Back End errors."""
    pass


class NotFoundError(BackEndError):
    """Generic class for all errors related to not found."""
    __slots__ = ("missing_col",)

    def __init__(self, missing_col):
        self.missing_col = missing_col


class AlreadyExistsError(BackEndError):
    """Generic class for all errors with duplicate row."""
    __slots__ = ("exists_col",)

    def __init__(self, dup_col):
        self.exists_col = dup_col


class UserAlreadyExistsError(AlreadyExistsError):
    def __init__(self):
        self.dup_col = User.username


class EmailAlreadyExistsError(AlreadyExistsError):
    def __init__(self):
        self.dup_col = User.email


class UsernameDoNotExistsError(NotFoundError):
    def __init__(self):
        self.missing_col = User.username


class EmailDoNotExistsError(NotFoundError):
    def __init__(self):
        self.missing_col = User.email


class UserPasswordNoMatchError(BackEndError):
    pass


class LoginSessionExpired(BackEndError):
    pass
