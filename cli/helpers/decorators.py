"""
Custom helper decorators module
"""
import asyncio
from base64 import b64encode, b64decode
from functools import wraps


def decode_pass(passwd):
    """Decode base64 string.
    """
    return b64decode(passwd.encode('ascii')).decode('ascii')


def encode_pass(f):
    """Encode password with base64.
    """

    @wraps(f)
    def enc(*args, **kwargs):
        if 'password' in kwargs.keys():
            kwargs['password'] = b64encode(
                kwargs['password'].encode('ascii')).decode('ascii')
        return f(*args, **kwargs)

    return enc


def url_validator(f):
    """validates URL format
    """

    @wraps(f)
    def validator(*args, **kwargs):
        for url in kwargs['urls']:
            assert f"https://intranet.hbtn.io/projects/{url.split('/')[-1]}" == url, "Not a valid URL"
        return f(*args, **kwargs)

    return validator


def handle_errors(f):
    """Handles errors
    """

    @wraps(f)
    def error(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except (AssertionError, BaseException) as err:
            exit(f"Error: {err}")

    return error


def coroutine(f):
    """Runs a coroutine
    """

    @wraps(f)
    @handle_errors
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return wrapper
