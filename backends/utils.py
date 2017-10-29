from functools import wraps
from os import environ

from backends.exceptions import ErrorException


def wrap_exception(exception_type, error_message):
    def _typed_exception_wrapper(func):
        @wraps(func)
        def _adapt_exception_types(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as ex:
                raise ErrorException(error_message) from ex
        return _adapt_exception_types
    return _typed_exception_wrapper


def getenv_required(key):
    try:
        return environ[key]
    except KeyError:
        raise ErrorException(
            'Required environment variable %s not set' % key)


def getenv_int(key, default):
    try:
        value = environ[key]
    except KeyError:
        return default

    try:
        return int(value)
    except ValueError:
        raise ErrorException(
            'Environment variable %s with value %s '
            'is not convertible to int' % (key, value))


def filters_match(metadata, filters, fdefaults):
    for metadata_key, filter_value in filters.items():
        try:
            metadata_value = metadata[metadata_key]
        except KeyError:
            metadata_value = fdefaults.get(metadata_key)

        if metadata_value != filter_value:
            return False

    return True
