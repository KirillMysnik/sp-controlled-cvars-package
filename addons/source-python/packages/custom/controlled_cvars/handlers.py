from colors import Color
from core import GAME_NAME
from engines.sound import Sound, StreamSound

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


def _find_best_sound_class(sample):
    if GAME_NAME not in ("csgo",):
        return Sound

    sample = sample.lower()

    if sample.endswith(".wav"):  # StreamSound won't work for wav files anyways
        return Sound

    if sample.startswith("music/"):  # No need for StreamSound
        return Sound

    return StreamSound


def sound_handler(cvar):
    sample = cvar.get_string()
    return _find_best_sound_class(sample)(sample)


def sound_nullable_handler(cvar):
    sample = cvar.get_string()
    if not sample:
        return None

    return _find_best_sound_class(sample)(sample)


def string_handler(cvar):
    return cvar.get_string()
