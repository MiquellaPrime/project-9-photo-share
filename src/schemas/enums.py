import enum


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
