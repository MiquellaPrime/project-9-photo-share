from pwdlib import PasswordHash


class PasswordContext:
    """Class for hashing and validating passwords"""

    def __init__(self, scheme: str = "argon2"):
        self._ctx = PasswordHash(scheme)

    def hash_password(self, password: str) -> str:
        return self._ctx.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return self._ctx.verify(password, hashed)


pwd_context = PasswordContext()
