from passlib.context import CryptContext


class PasswordContext:
    """ "Class for hashing and validating passwords"""

    def __init__(self, password):
        self._ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._ctx.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return self._ctx.verify(password, hashed)


pwd_context = PasswordContext()
