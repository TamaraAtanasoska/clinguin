"""
This module contains various utils for tkinter-elements, which reduce code size, etc.
"""
from .attribute_names import AttributeNames
from .callback_names import CallbackNames
from .call_back_definition import CallBackDefinition

from .extension_class import ExtensionClass
from .layout_follower import LayoutFollower
from .layout_controller import LayoutController
from .configure_size import ConfigureSize
from .configure_border import ConfigureBorder
from .configure_font import ConfigureFont

__all__ = [
    AttributeNames.__name__,
    CallbackNames.__name__,
    CallBackDefinition.__name__,
    LayoutFollower.__name__,
    ExtensionClass.__name__,
    LayoutController.__name__,
    ConfigureSize.__name__,
    ConfigureBorder.__name__,
    ConfigureFont.__name__,
]
