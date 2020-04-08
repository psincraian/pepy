from passlib.handlers.pbkdf2 import pbkdf2_sha256

from pepy.domain.model import Password, HashedPassword


class AdminPasswordChecker:
    def __init__(self, admin_password: HashedPassword):
        self._admin_password = admin_password

    def check(self, password: Password) -> bool:
        return pbkdf2_sha256.verify(password.password, self._admin_password.password)
