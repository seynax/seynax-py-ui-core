from tkinter    import Tk
from tkinter.font   import Font
from typing         import Type

from utils.attributes.dict_utils        import merge
from utils.attributes.attribute_utils   import non_none, attempt_call, attempt_call_method


class Theme:
    def __init__(self, parent, font_size: int = 22, background: str = 'black', foreground: str = 'white'):
        self.parent     = parent
        self.font_size  = font_size
        self.font = Font(font='', size=self.font_size)
        self.background = background
        self.foreground = foreground

    def set_color(self, background: str, foreground: str):
        self.background = background
        self.foreground = foreground

        if hasattr(self.parent, 'update_color'):
            self.parent.update_color()

    def set_size(self, size: int):
        self.font.config(size=size)

    def increase_size(self, increment: int = 4):
        self.font_size += increment
        self.font.config(size=self.font_size)

    def decrease_size(self, decrement: int = 4):
        self.font_size -= decrement
        self.font.config(size=self.font_size)


class UIManager:
    def __init__(self, window: Tk, theme: Theme, parent = None):
        self.window = window
        self.theme = theme

        self.parent = non_none(parent, window)
        self.child_list = []

    def config(self, **args):
        self._execute('config', **args)

    def _execute(self, name: str, **args):
        for child in self.child_list:
            attempt_call_method(method_source       = child,
                                method_name         = name,
                                forced_parameters   = args,
                                force_unpack              = True)

    def _execute_diverge(self, name: str, tkinter_name: str, **args):
        for child in self.child_list:
            if isinstance(child, UIManager):
                attempt_call_method(method_source       = child,
                                    method_name         = name,
                                    forced_parameters   = args,
                                    unpack              = False)
            else:
                attempt_call_method(method_source       = child,
                                    method_name         = tkinter_name,
                                    forced_parameters   = args,
                                    unpack              = False)

    def update_color(self):
        self._execute_diverge('update_color','config',
                                    background = self.theme.background,
                                    foreground = self.theme.foreground)

    def add(self, child, **constructor_arguments):
        if child is None:
            return child

        parent = self.parent
        if hasattr(self, 'root'):
            parent = self.root

        try:
            if isinstance(child, Type) and issubclass(child, UIManager):
                child = attempt_call(_callable=child, forced_parameters=merge(constructor_arguments, {
                    'window': self.window,
                    'theme': self.theme,
                    'parent': parent
                }), force_unpack=True)
            else:
                child = attempt_call(_callable=child, forced_parameters=merge(constructor_arguments, {
                    'master': parent
                }), force_unpack=True)
                attempt_call_method(method_source=child,
                                    method_name='config',
                                    forced_parameters={
                                        'background': self.theme.background,
                                        'foreground': self.theme.foreground,
                                        'font': self.theme.font
                                    },
                                    unpack=False)

                attempt_call_method(child, 'pack')
        except Exception:
            pass

        self.child_list.append(child)

        return child
