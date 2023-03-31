"""
Contains the tkinter-gui class.
"""
from clinguin.show_frontend_syntax_enum import ShowFrontendSyntaxEnum
from clinguin.client import AbstractFrontend

from .tkinter_elements import *
from .tkinter_utils import *


class TkinterFrontend(AbstractFrontend):
    """
    Class that inherits from AbstractFrontend and is therefore a dynamically loaded class, if it shall be used to render the Frontend. It defines what to do for each element.
    """

    def __init__(self, base_engine, args):
        super().__init__(base_engine, args)

        self.elements = {}
        self.first = True

    @classmethod
    def register_options(cls, parser):
        parser.description = (
            "This GUI is based on the Python-Tkinter package and uses tkinter elements."
        )

    @classmethod
    def available_syntax(cls, show_level):
        def append_dict(description, _dict, type_name):

            for key in _dict.keys():
                description = description + "    |- " + key + "\n"
                if show_level == ShowFrontendSyntaxEnum.FULL:
                    if "description" in _dict[key]:
                        # Specific has higher priority
                        description = description + "      |- Description: "
                        description = description + ": " + _dict[key]["description"]
                        description = description + "\n"
                    elif key in AttributeNames.descriptions:
                        # General lesser priority
                        description = description + "      |- Description: "
                        description = (
                            description + ": " + AttributeNames.descriptions[key]
                        )
                        description = description + "\n"
                    elif key in CallbackNames.descriptions:
                        description = description + "      |- Description: "
                        description = (
                            description + ": " + CallbackNames.descriptions[key]
                        )
                        description = description + "\n"

                    if type_name in _dict[key]:
                        description = description + "      |- Possible-Values: "
                        description = (
                            description + _dict[key][type_name].description() + "\n"
                        )

            return description

        description = (
            "Here one finds the supported attributes and callbacks of the TkinterFrontend and further a definition of the syntax:\n"
            + "There are three syntax elements:\n\n"
            + "element(<ID>, <TYPE>, <PARENT>) : To define an element\n"
            + "attribute(<ID>, <KEY>, <VALUE>) : To define an attribute for an element (the ID is the ID of the corresponding element)\n"
            + "callback(<ID>, <ACTION>, <POLICY>) : To define a callback for an element (the ID is the ID of the corresponding element)\n\n"
            + "The following list shows for each <TYPE> the possible attributes and callbacks:\n"
        )

        class_list = RootCmp.__subclasses__()

        description = description + "|--------------------------------\n"
        for c in class_list:
            description = description + "|- " + c.__name__ + "\n"

            attributes = c.get_attributes()
            if len(attributes.keys()) > 0:
                description = description + "  |- attributes\n"
                description = append_dict(description, attributes, "value_type")

            callbacks = c.get_callbacks()
            if len(callbacks.keys()) > 0:
                description = description + "  |- callbacks\n"
                description = append_dict(description, callbacks, "policy_type")
            description = description + "|--------------------------------\n"

        return description

    def window(self, id, parent, attributes, callbacks):

        if self.first:
            window = Window(
                self._args, id, parent, attributes, callbacks, self._base_engine
            )
            window.add_component(self.elements)
        else:
            keys = list(self.elements.keys()).copy()
            for key in keys:
                if str(key) == str(id):
                    continue

                if str(key) in self.elements:
                    self.elements[str(key)].forget_children(self.elements)
                    del self.elements[str(key)]

    def container(self, id, parent, attributes, callbacks):
        container = Container(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        container.add_component(self.elements)

    def dropdown_menu(self, id, parent, attributes, callbacks):
        menu = Dropdownmenu(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        menu.add_component(self.elements)

    def dropdown_menu_item(self, id, parent, attributes, callbacks):
        menu = DropdownmenuItem(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        menu.add_component(self.elements)

    def label(self, id, parent, attributes, callbacks):
        label = Label(self._args, id, parent, attributes, callbacks, self._base_engine)
        label.add_component(self.elements)

    def button(self, id, parent, attributes, callbacks):
        button = Button(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        button.add_component(self.elements)

    def menu_bar(self, id, parent, attributes, callbacks):
        menubar = MenuBar(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        menubar.add_component(self.elements)

    def menu_bar_section(self, id, parent, attributes, callbacks):
        menubar = MenuBarSection(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        menubar.add_component(self.elements)

    def menu_bar_section_item(self, id, parent, attributes, callbacks):
        menubar = MenuBarSectionItem(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        menubar.add_component(self.elements)

    def message(self, id, parent, attributes, callbacks):
        message = Message(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        message.add_component(self.elements)

    def canvas(self, id, parent, attributes, callbacks):
        canvas = Canvas(
            self._args, id, parent, attributes, callbacks, self._base_engine
        )
        canvas.add_component(self.elements)

    def draw(self, id):
        self.first = False
        self.elements[id].get_element().mainloop()
