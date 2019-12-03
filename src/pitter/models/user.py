from django.db import models

from pitter.models.base import default_uuid_id
from pitter.utils.hashers import PasswordHash


class User(models.Model):
    id = models.CharField(default=default_uuid_id, primary_key=True, editable=False, max_length=256)
    login = models.CharField(
        max_length=64,
        blank=False,
        unique=True,
        error_messages={
            'unique': "A user with this login already exists."
        }
    )
    password = models.CharField(max_length=256, blank=False)
    profile_name = models.CharField(max_length=64, blank=True)
    email = models.CharField(max_length=128, blank=True)
    email_notifications_enabled = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now=True)
    last_action_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            login=self.login,
            profile_name=self.profile_name if self.profile_name else None,
            joined_at=self.joined_at,
            last_action_at=self.last_action_at,
        )

    @staticmethod
    def get(**kwargs):
        return User.objects.get(**kwargs)

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

    @classmethod
    def register_new_user(cls, login, password):
        user, created = User.objects.get_or_create(login=login)
        if created:
            user.set_password(password)
            user.save()

        return user, created

    def patch(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save(update_fields=kwargs.keys())
        return self

    def set_password(self, raw_password):
        self.password = PasswordHash.make_password(raw_password)

    def check_password(self, raw_password):
        return PasswordHash.check_password(raw_password, self.password)

    def __str__(self):
        return self.login

    def __repr__(self):
        return f"<User(id={self.id}, login={self.login}, profile_name={self.profile_name}), " \
               f"email={self.email}, email_notifications_enabled={self.email_notifications_enabled}, " \
               f"joined_at={self.joined_at}, last_action_at={self.last_action_at}>"
