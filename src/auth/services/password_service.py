import bcrypt


class PasswordManager:
    def hash_password(self, password: str) -> bytes:
        """
        Хэширует пароль с помощью bcrypt.

        Args:
            password (str): Обычный пароль.

        Returns:
            bytes: Хэшированный пароль.
        """
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    def validate_password(self, password: str, hashed_password: bytes) -> bool:
        """
        Проверяет, совпадает ли обычный пароль с хэшированным.

        Args:
            password (str): Обычный пароль.
            hashed_password (bytes): Хэшированный пароль.

        Returns:
            True: если пароли совпадают,
            False: если пароли разные.
        """
        return bcrypt.checkpw(password.encode(), hashed_password)


passwords_manager = PasswordManager()


def get_password_manager() -> PasswordManager:
    return passwords_manager
