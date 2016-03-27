from config.manager import ConfigManager
from core import AutoUnload, echo_console
from cvars.flags import ConVarFlags
from events import Event


class InvalidValue(Exception):
    pass


class ControlledConfigManager(AutoUnload, ConfigManager):
    def __init__(
            self, filepath, cvar_prefix='', indention=3, max_line_length=79):

        super().__init__(filepath, cvar_prefix, indention, max_line_length)

        self._saved_values = {}
        self._handlers = {}

    def controlled_cvar(self, handler, name, default=0, description='', flags=0,
             min_value=None, max_value=None):

        flags |= ConVarFlags.NOTIFY
        cvar = super().cvar(
            name, default, description, flags, min_value, max_value)

        self._handlers[name] = handler

        try:
            self._saved_values[name] = handler(cvar)
        except InvalidValue:
            self._saved_values[name] = None

        if cvar.name in cvar_mapping:
            raise ValueError(
                "'{}' already has a handler attached".format(cvar.name))

        cvar_mapping[cvar.name] = cvar, self

        return cvar

    def _cvar_changed(self, cvar):
        name = cvar.name[len(self.cvar_prefix):]
        try:
            value = self._handlers[name](cvar)
        except InvalidValue:
            return False

        self._saved_values[name] = value
        return True

    def __getitem__(self, name):
        return self._saved_values[name]

    def _unload_instance(self):
        for name in self._saved_values.keys():
            full_name = self.cvar_prefix + name
            del cvar_mapping[full_name]


cvar_mapping = {}


@Event('server_cvar')
def on_server_cvar(game_event):
    if game_event['cvarname'] not in cvar_mapping:
        return

    cvar, config_manager = cvar_mapping[game_event['cvarname']]

    if config_manager._cvar_changed(cvar):
        echo_console("Variable was updated successfully")

    else:
        echo_console("Failed to update variable with the given value")
