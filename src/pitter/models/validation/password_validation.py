from pitter.exceptions import ValidationError


def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.
    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    password_validators = [MinimumLengthValidator(), NumericPasswordValidator()]
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)


def password_changed(password, user=None, password_validators=None):
    """
    Inform all validators that have implemented a password_changed() method
    that the password has been changed.
    """
    password_validators = [MinimumLengthValidator(), NumericPasswordValidator()]
    for validator in password_validators:
        password_changed = getattr(validator, 'password_changed', lambda *a: None)
        password_changed(password, user)


class MinimumLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"This password is too short. It must contain at least %{self.min_length} character.",
                status_code=400,
                payload={'min_length': self.min_length},
            )

    def get_help_text(self):
        return f"Your password must contain at least %{self.min_length} character."


class NumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError("This password is entirely numeric.", status_code=400)

    def get_help_text(self):
        return 'Your password can’t be entirely numeric.'
