import re
import ipaddress

from django.utils.ipv6 import is_valid_ipv6_address

from pitter.exceptions import ValidationError


class LoginValidator:  # pylint: disable=too-few-public-methods
    compiled_regex = re.compile(r'^\w[\w.]+\w\Z')
    message = 'Enter a valid username. This value may contain only letters, ' \
              'numbers, and ./_ characters and should start with letter and end ' \
              'with letter.'
    status_code = 400
    flags = 0

    @classmethod
    def validate(cls, value):
        regex_matches = cls.compiled_regex.search(str(value))
        if not regex_matches:
            raise ValidationError(cls.message, status_code=cls.status_code)


def validate_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise ValidationError('Enter a valid IPv4 address.', status_code=400)


def validate_ipv6_address(value):
    if not is_valid_ipv6_address(value):
        raise ValidationError('Enter a valid IPv6 address.', status_code=400)


def validate_ipv46_address(value):
    try:
        validate_ipv4_address(value)
    except ValidationError:
        try:
            validate_ipv6_address(value)
        except ValidationError:
            raise ValidationError('Enter a valid IPv4 or IPv6 address.', status_code=400)


class EmailValidator:
    message = 'Enter a valid email address.'
    status_code = 400
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE)
    domain_regex = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
        re.IGNORECASE)
    literal_regex = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r'\[([A-f0-9:\.]+)\]\Z',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    @classmethod
    def validate(cls, value):
        if not value or '@' not in value:
            raise ValidationError(cls.message, status_code=cls.status_code)

        user_part, domain_part = value.rsplit('@', 1)

        if not cls.user_regex.match(user_part):
            raise ValidationError(cls.message, status_code=cls.status_code)

        if (domain_part not in cls.domain_whitelist and not cls.validate_domain_part(domain_part)):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode('idna').decode('ascii')
            except UnicodeError:
                pass
            else:
                if cls.validate_domain_part(domain_part):
                    return
            raise ValidationError(cls.message, status_code=cls.status_code)

    @classmethod
    def validate_domain_part(cls, domain_part):
        if cls.domain_regex.match(domain_part):
            return True

        literal_match = cls.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match.group(1)
            try:
                validate_ipv46_address(ip_address)
                return True
            except ValidationError:
                pass
        return False


class PasswordValidator:
    min_length = 8

    @classmethod
    def validate(cls, password):
        cls.validate_minimum_length(password)
        cls.validate_numeric_password(password)

    @classmethod
    def validate_minimum_length(cls, password):
        if len(password) < cls.min_length:
            raise ValidationError(
                message=f"This password is too short. It must contain at least {cls.min_length} character.",
                status_code=400,
                payload={'min_length': cls.min_length},
            )

    @classmethod
    def validate_numeric_password(cls, password):
        if password.isdigit():
            raise ValidationError(message="This password is entirely numeric.", status_code=400)
