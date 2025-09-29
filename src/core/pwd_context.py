from passlib.context import CryptContext


class PasswordContext:
    """Class for hashing and validating passwords"""

    def __init__(self, schemes: list[str], deprecated: str):
        self._ctx = CryptContext(schemes=schemes, deprecated=deprecated)

    def hash_password(self, password: str) -> str:
        return self._ctx.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return self._ctx.verify(password, hashed)


pwd_context = PasswordContext(schemes=["bcrypt"])
