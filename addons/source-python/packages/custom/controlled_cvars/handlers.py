from colors import Color
from engines.sound import Sound

from . import InvalidValue


def bool_handler(cvar):
    try:
        return bool(int(cvar.get_string()))
    except ValueError:
        raise InvalidValue


def color_handler(cvar):
    try:
        return Color(*map(int, cvar.get_string().split(',')))

    except (OverflowError, TypeError, ValueError):
        raise InvalidValue


def float_handler(cvar):
    try:
        return float(cvar.get_string())
    except ValueError:
        raise InvalidValue


def int_handler(cvar):
    try:
        return int(cvar.get_string())
    except ValueError:
        raise InvalidValue


def list_handler(cvar):
    return cvar.get_string().strip(',').split(',')


def sound_handler(cvar):
    return Sound(cvar.get_string())


def sound_nullable_handler(cvar):
    val = cvar.get_string()
    return None if val == "" else Sound(val)


def string_handler(cvar):
    return cvar.get_string()
