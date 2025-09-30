from enum import Enum


class UserRoles(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
