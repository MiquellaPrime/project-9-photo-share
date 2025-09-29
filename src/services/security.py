from pwdlib import PasswordHash


class PasswordHashService:
    """Service for hashing and verifying passwords."""

    password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password=password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password=password, hash=hashed_password)
