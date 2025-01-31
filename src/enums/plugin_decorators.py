from functools import wraps

from src.enums.enums import PluginType


def plugin_type(plugin_type: PluginType):
    """
    Decorator to assign a type to a plugin.

    Args:
        plugin_type (PluginType): The type of the plugin (e.g., OXY or OSMO).
    """

    def decorator(cls):
        original_init = cls.__init__

        @wraps(cls)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)  # Call the original __init__ method
            self.plugin_type = plugin_type  # Set the plugin type

        cls.__init__ = new_init
        return cls

    return decorator
