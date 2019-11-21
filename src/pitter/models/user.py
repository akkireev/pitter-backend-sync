from __future__ import annotations

import unicodedata

from django.contrib import auth
from django.core.validators import EmailValidator
from django.db import models
from django.utils.crypto import salted_hmac, get_random_string

from pitter.models.base import default_uuid_id
from pitter.models.validation import password_validation
from pitter.models.validation.login_validation import UnicodeLoginValidator
from pitter.utils.hashers import PasswordHash


class UserManager(models.Manager):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, login):
        return self.get(**{'login': login})

    def create_user(self, login, email, password, **extra_fields):
        """
        Create and save a user with the given login, email, and password.
        """
        if not login:
            raise ValueError('The given login must be set')
        email = self.normalize_email(email)
        login = self.model.normalize_login(login)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(models.Model):
    objects = UserManager()

    login_validator = UnicodeLoginValidator()
    email_validator = EmailValidator()

    id = models.CharField(default=default_uuid_id, primary_key=True, editable=False, max_length=256)
    login = models.CharField(
        max_length=64,
        blank=False,
        unique=True,
        validators=[login_validator],
        error_messages={
            'unique': "A user with this login already exists."
        }
    )
    password = models.CharField(max_length=64, blank=False)
    profile_name = models.CharField(max_length=64, blank=True)
    email = models.CharField(
        max_length=128,
        blank=True,
        validators=[email_validator]
    )
    email_notifications_enabled = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now=True)
    last_action_at = models.DateTimeField(auto_now=True)

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    def __str__(self):
        return self.get_login()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_login(self):
        """Return the login for this User."""
        return getattr(self, 'login')

    def clean(self):
        setattr(self, 'login', self.normalize_login(self.get_login()))

    def natural_key(self):
        return (self.get_login(),)

    def set_password(self, raw_password):
        self.password = PasswordHash.make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return PasswordHash.check_password(raw_password, self.password, setter)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return PasswordHash.is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "pitter.models.user.User.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        return 'email'

    @classmethod
    def normalize_login(cls, login):
        return unicodedata.normalize('NFKC', login) if isinstance(login, str) else login
