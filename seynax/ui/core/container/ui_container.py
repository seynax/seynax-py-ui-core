from tkinter import Frame
from typing import Union, Any, Type, Dict, Literal, Self

from utils.attributes.attribute_utils import attempt_call_method

from seynax.ui.core.components.components import Component
from seynax.ui.core.ui_manager import Theme
from seynax.ui.core.ui_window import UIWindow


class UIContainer:
    def __init__(self,
                 window: UIWindow,
                 theme: Theme,
                 parent: Union[Self, Component] = None,
                 **kwargs):
        self.window         = window
        self.theme          = theme
        self.parent         = parent
        self.component_list = []
        self.main_handle    = None

    def component(self,
                  handle: Union[Any, Type] = None,
                  config_args: Dict = None,
                  placement_type: Literal['pack', 'place', 'grid'] = 'pack',
                  placement_args: Dict = None,
                  **kwargs) -> Component:
        component = Component(self.window, self.theme, handle, self.main_handle,
                              config_args, placement_type, placement_args, **kwargs)
        self.component_list.append(component)

        if self.main_handle is None:
            self.main_handle = component

        return component

    def container(self, **kwargs):
        container = UIContainer(self.window, self.theme, self, **kwargs)
        self.component_list.append(container)

        if self.main_handle is None:
            self.main_handle = container

        return container

    def update_color(self):
        self._execute_diverge('update_color', 'config',
                                background=self.theme.background,
                                foreground=self.theme.foreground)

    def _execute(self, name: str, **args):
        for child in self.component_list:
             attempt_call_method(method_source=child,
                                 method_name=name,
                                 forced_parameters=args,
                                 force_unpack=True)

    def _execute_diverge(self, name: str, tkinter_name: str, **args):
        for child in self.component_list:
            if isinstance(child, Component):
                attempt_call_method(method_source=child,
                                    method_name=name,
                                    forced_parameters=args,
                                    unpack=False)
            else:
                attempt_call_method(method_source=child,
                                    method_name=tkinter_name,
                                    forced_parameters=args,
                                    unpack=False)


class UIRootContainer(UIContainer):
    def __init__(self,
                 window,
                 theme: Theme,
                 parent: Component = None,
                 handle: Union[Any, Type] = None,
                 config_args: Dict = None,
                 placement_type: Literal['pack', 'place', 'grid'] = 'pack',
                 placement_args: Dict = None,
                 **kwargs):
        super(UIRootContainer).__init__(window, theme, parent)
        self.root = self.component(handle, config_args, placement_type, placement_args, **kwargs)

    def component(self,
                  handle: Union[Any, Type] = None,
                  config_args: Dict = None,
                  placement_type: Literal['pack', 'place', 'grid'] = 'pack',
                  placement_args: Dict = None,
                  **kwargs) -> Component:
        return super().component(handle, config_args, placement_type, placement_args, master=self.root, **kwargs)

class UIFrame(UIRootContainer):
    def __init__(self,
                 window,
                 theme: Theme,
                 parent = None,
                 config_args: Dict = None,
                 placement_type: Literal['pack', 'place', 'grid'] = 'pack',
                 placement_args: Dict = None,
                 **kwargs):
        super().__init__(window, theme, parent, Frame, config_args, placement_type, placement_args, **kwargs)
