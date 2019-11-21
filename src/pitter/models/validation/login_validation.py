import re
import ipaddress

from django.utils.deconstruct import deconstructible
from django.utils.functional import SimpleLazyObject
from django.utils.ipv6 import is_valid_ipv6_address

from pitter.exceptions import ValidationError


def _lazy_re_compile(regex, flags=0):
    """Lazily compile a regex with flags."""

    def _compile():
        # Compile the regex if it was not passed pre-compiled.
        if isinstance(regex, str):
            return re.compile(regex, flags)
        else:
            assert not flags, "flags must be empty if regex is passed pre-compiled"
            return regex

    return SimpleLazyObject(_compile)


@deconstructible
class RegexValidator:
    regex = ''
    message = 'Enter a valid value.'
    status_code = 400
    inverse_match = False
    flags = 0

    def __init__(self, regex=None, message=None, code=None, inverse_match=None, flags=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if inverse_match is not None:
            self.inverse_match = inverse_match
        if flags is not None:
            self.flags = flags
        if self.flags and not isinstance(self.regex, str):
            raise TypeError("If the flags are set, regex must be a regular expression string.")

        self.regex = _lazy_re_compile(self.regex, self.flags)

    def __call__(self, value):
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """
        regex_matches = self.regex.search(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches
        if invalid_input:
            raise ValidationError(self.message, status_code=self.status_code)

    def __eq__(self, other):
        return (
                isinstance(other, RegexValidator) and
                self.regex.pattern == other.regex.pattern and
                self.regex.flags == other.regex.flags and
                (self.message == other.message) and
                (self.code == other.code) and
                (self.inverse_match == other.inverse_match)
        )


@deconstructible
class UnicodeLoginValidator(RegexValidator):
    regex = r'^[\w.@]+\Z'
    message = 'Enter a valid username. This value may contain only letters, ' \
              'numbers, and @/./_ characters.'
    flags = 0


def validate_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise ValidationError(_('Enter a valid IPv4 address.'), status_code=400)


def validate_ipv6_address(value):
    if not is_valid_ipv6_address(value):
        raise ValidationError(_('Enter a valid IPv6 address.'), status_code=400)


def validate_ipv46_address(value):
    try:
        validate_ipv4_address(value)
    except ValidationError:
        try:
            validate_ipv6_address(value)
        except ValidationError:
            raise ValidationError(_('Enter a valid IPv4 or IPv6 address.'), status_code=400)


class EmailValidator:
    message = 'Enter a valid email address.'
    status_code = 400
    user_regex = _lazy_re_compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE)
    domain_regex = _lazy_re_compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
        re.IGNORECASE)
    literal_regex = _lazy_re_compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r'\[([A-f0-9:\.]+)\]\Z',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    def __init__(self, message=None, status_code=None, whitelist=None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def __call__(self, value):
        if not value or '@' not in value:
            raise ValidationError(self.message, status_code=self.status_code)

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, status_code=self.status_code)

        if (domain_part not in self.domain_whitelist and
                not self.validate_domain_part(domain_part)):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode('idna').decode('ascii')
            except UnicodeError:
                pass
            else:
                if self.validate_domain_part(domain_part):
                    return
            raise ValidationError(self.message, status_code=self.status_code)

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match.group(1)
            try:
                validate_ipv46_address(ip_address)
                return True
            except ValidationError:
                pass
        return False
