from pathlib import Path
import secrets
from logging import getLogger

logger = getLogger()


class Credentials:
    salt_path = Path("salt.txt")
    password_path = Path("password.txt")

    def __init__(self, username: str = "") -> None:
        self.user_path = Path(username)

    def validate_username(self) -> bool:
        if self.salt_path == "":
            return False
        elif self.user_path.exists() and Path(self.user_path, self.salt_path).exists():
            return True
        else:
            return False

    @staticmethod
    def generate_salt() -> bytes:
        return secrets.token_bytes(8)

    def get_salt(self) -> bytes:
        return Path(self.user_path, self.salt_path).read_bytes()

    @staticmethod
    def calculate_password_hash(password: str, salt: bytes) -> str:
        return str(hash(password.encode() + salt))

    def read_password(self) -> str:
        return Path(self.user_path, self.password_path).read_text()

    def create_user(self, password: str) -> None:
        self.user_path.mkdir()
        salt = self.generate_salt()
        Path(self.user_path, self.salt_path).write_bytes(salt)

        Path(self.user_path, self.password_path).write_text(
            self.calculate_password_hash(password=password, salt=salt)
        )

    def validate_user(self, password: str) -> bool:
        result = (
            self.calculate_password_hash(password=password, salt=self.get_salt())
            == self.read_password()
        )
        logger.info(result)
        return result
