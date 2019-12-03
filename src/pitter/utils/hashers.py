import bcrypt

from django.conf import settings
from django.utils.crypto import constant_time_compare


class BCryptSHA256PasswordHasher:
    rounds = 12

    def salt(self):
        return bcrypt.gensalt(self.rounds)

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, encoded.encode('ascii'))
        return constant_time_compare(encoded, encoded_2)

    @staticmethod
    def encode(password, salt):
        password = password.encode('ascii')
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password.decode('ascii')


class PasswordHash:
    hasher = BCryptSHA256PasswordHasher()

    @classmethod
    def check_password(cls, password, encoded, setter=None):
        if password is None:
            return False

        pepper_password = cls.add_pepper(password)
        is_correct = cls.hasher.verify(pepper_password, encoded)

        if setter and is_correct:
            setter(password)
        return is_correct

    @classmethod
    def make_password(cls, password, salt=None):
        salt = salt or cls.hasher.salt()
        pepper_password = cls.add_pepper(password)
        return cls.hasher.encode(pepper_password, salt)

    @classmethod
    def add_pepper(cls, password):
        return f"{password}{settings.SECRET_PASSWORD_PEPPER}"
