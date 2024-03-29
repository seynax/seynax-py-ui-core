from tkinter                            import Label, Text, Menu, Frame, Button

from tkinter.constants                  import X, Y,  BOTH
from tkinter.constants                  import TOP, BOTTOM, LEFT, RIGHT
from tkinter.constants                  import NW, SW, NE, SE
from tkinter.constants                  import N, S, W, E
from typing import Any, Type, Union, Literal, Dict

from utils.attributes.attribute_utils   import non_none, attempt_call_method, attempt_call
from utils.attributes.dict_utils        import merge

from seynax.ui.core.keyboard            import keyboard
from seynax.ui.core.ui_manager          import Theme

class EmptyComponent:
    pass


'''
    Component: Tkinter component manager with utilities methods
    Component.handle: Tkinter component
    w<name>(): return value         from handle.winfo_<name>()
    t<name>(): execute and return   from handle.<name>()
'''
class Component(EmptyComponent):
    def __init__(self,
                 window,
                 theme: Theme,
                 handle: Union[Any, Type],
                 parent: EmptyComponent = None,
                 config_args: Dict = None,
                 placement_type: Literal['pack', 'place', 'grid'] = 'pack',
                 placement_args: Dict = None,
                 **kwargs):
        self.window         = window
        self.theme          = theme
        self.parent         = parent

        self.parent         = non_none(parent, self.window)

        self.constructor_args   = kwargs
        self.config_args        = non_none(config_args, {})
        self.placement_type     = placement_type
        self.placement_args     = non_none(placement_args, {})

        # Handle
        self.handle = self._initialize_handle(handle)

    def _initialize_handle(self, handle):
        if handle is None:
            print('!')
            return handle

        handle = attempt_call(_callable=handle, forced_parameters=merge(self.constructor_args, {
            'master': None if not hasattr(self.window, 'handle') else self.window.handle
        }), force_unpack=True)

        settings = {'background': self.theme.background,
                    'foreground': self.theme.foreground,
                    'font': self.theme.font}

        for name, value in settings.items():
            attempt_call_method(method_source=handle,
                                method_name='config',
                                forced_parameters={
                                    name: value
                                },
                                unpack=False)
        attempt_call_method(handle, self.placement_type, **self.placement_args)

        for method_name in dir(handle):
            if method_name.startswith('winfo'):
                setattr(self,
                        f'w{method_name.replace("winfo_", "")}',
                        getattr(handle, method_name))
                continue

            if method_name.startswith('_'):
                continue

            setattr(self,
                    f't{method_name}',
                    getattr(handle, method_name))
            print(method_name)

        return handle




class ComponentLabel(Component):
    def __init__(self, window, theme: Theme, parent = None, **args):
        super().__init__(window, theme, parent)
        self.label = self.add(Label, **args)

    def update_text(self, text: str = ''):
        self.label.config(text=text)


class ComponentTextBox(Component):
    def __init__(self, window, theme: Theme, text: str = '', parent = None, **args):
        super().__init__(window, theme, parent)
        self.text = text
        self.box = self.add(Text, **args)
        self.box.insert('end', text)

    def clear(self):
        self.box.delete(1.0, 'end')

    def set(self, text: str = ''):
        self.clear()
        self.box.insert('end', text)


class ComponentNativeMenu(Component):
    def __init__(self, window, theme: Theme, parent = None, **args):
        super().__init__(window, theme, parent)
        self.menu = self.add(Menu, **args)
        self.menu.config(background='yellow')
        self.root = self.menu
        # TODO improve this to avoid exception
        try:
            self.parent.config(menu=self.menu)
        except Exception:
            pass

    def start_menu(self, **args):
        sub_menu = self.add(ComponentNativeMenu, **args)

        return sub_menu

    def cascade(self, **args):
        sub_menu = self.add(ComponentNativeMenu, **args)

        self.menu.add_cascade(label=sub_menu.menu.cget('title'), menu=sub_menu.menu)

        return sub_menu

    def command(self, **args):
        if 'accelerator' in args and 'command' in args:
            self.window_handle.bind_all(keyboard.translate(args['accelerator']), lambda event: args['command']())
        args['font'] = self.theme.font
        self.menu.add_command(**args)


class ComponentMenuEntry(Component):
    def __init__(self, window, theme: Theme, parent = None, closeable: bool = True, **args):
        super().__init__(window, theme, parent)
        self.closeable = closeable

        self.args = args

        self.direction ='bottom'
        self.menu_child_list = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.menu_parent = None
        self.menu_current = None
        self.is_open = False
        self.opened_menu_index = -1

        self.root = self.add(Frame)
        self.grid = self.add(Frame, master=self.root)

        if 'text' in args:
            self.menu_parent = self.cascade(text=args['text'])
        else:
            self.menu_parent = None

    def cascade(self, show_accelerator: bool = None, accelerator: str = None, closeable: bool = True, **args):
        menu_entry = self.add(ComponentMenuEntry, closeable=closeable)
        if accelerator is not None:
            if show_accelerator is None:
                show_accelerator = hasattr(self.parent, 'parent') and hasattr(self.parent, 'menu_child_list') and len(self.parent.menu_child_list) > 1
            if show_accelerator:
                if 'text' in args:
                    args['text'] += '   ' + accelerator
            self.window_handle.bind(keyboard.translate(accelerator), lambda event: menu_entry.open())
        button = self.add(Button, master=self.grid, command=lambda: menu_entry.open(), **args)
        menu_entry.menu_parent = button
        if self.menu_current is None:
            self.menu_current = button
        self.menu_child_list.append(button)
        self.update_grid()
        self.fix_open()

        return menu_entry

    def fix_open(self):
        self.close()
        if not self.closeable:
            self.open()
        else:
            self.close()

    def update_grid(self):
        direction = 'horizontal'
        if hasattr(self.parent, 'update_grid') and len(self.menu_child_list) > 0:
                direction = 'vertical'

        side = 'bottom'
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'menu_child_list') and len(self.parent.parent.menu_child_list) > 1:
            side = 'right'

        # self.grid.grid_propagate(False)
        i = 0
        for menu_child in self.menu_child_list:
            if direction == 'vertical':
                self.grid.grid_rowconfigure(i, weight=1)
                self.grid.grid_columnconfigure(0, weight=1)
                menu_child.grid(row=i, column=0, sticky=N+S+W+E)
                menu_child.update()
                self.width = max(self.width, menu_child.winfo_width())
                self.height += menu_child.winfo_height()
            else:
                self.grid.grid_rowconfigure(0, weight=1)
                self.grid.grid_columnconfigure(i, weight=1)
                menu_child.grid(row=0, column=i, sticky=N+S+W+E)
                menu_child.update()
                self.width += menu_child.winfo_width()
                self.height = max(self.height, menu_child.winfo_height())
            i += 1

        if self.menu_parent is not None:
            self.menu_parent.update()
            if side == 'right':
                self.x = self.parent.root.winfo_x() + self.parent.root.winfo_width()
                self.y = self.menu_parent.winfo_y() - self.menu_parent.winfo_height() - self.menu_current.winfo_height() + self.grid.winfo_height()
                if hasattr(self.parent, 'menu_parent'):
                    self.y += self.parent.menu_parent.winfo_x() + self.parent.menu_parent.winfo_height()
            else:
                self.x = self.menu_parent.winfo_x()
                self.y = self.menu_parent.winfo_y() + self.menu_parent.winfo_height()

        self.grid.config(width=100, height=100)
        self.grid.grid(row=0, column=0, sticky='nswe')
        self.grid.update()

    def open(self):
        if len(self.menu_child_list) == 0 and self.closeable:
            self.close()
            return
        self.window.close_all_menu()
        if self.parent is not None and isinstance(self.parent, ComponentMenuEntry) and not self.parent.is_open:
            self.parent.open()
        self.is_open = True
        self.opened_menu_index = len(self.window.opened_menus)
        self.window.opened_menus[self.opened_menu_index] = self

        self.update_grid()
        self.root.place(x=self.x, y=self.y)

        self.window_handle.bind("<Key>",       self.key)
        self.window_handle.bind("<Button-1>",  self.mouse)

    def close(self):
        if not self.closeable:
            return
        self.is_open = False
        if self.opened_menu_index > 0:
            self.window.opened_menus.pop(self.opened_menu_index)

        if self.parent is not None and isinstance(self.parent, ComponentMenuEntry):
            self.window_handle.unbind("<Key>")
            self.window_handle.unbind("<Button-1>")
            if not self.parent.cursor_is_in():
                self.parent.close()
            else:
                self.window_handle.bind("<Key>",       self.parent.key)
                self.window_handle.bind("<Button-1>",  self.parent.mouse)

        self.root.place_forget()

    def key(self, event):
        pass

    def mouse(self, event):
        if not self.cursor_is_in():
            self.close()

    def cursor_is_in(self):
        x = self.window_handle.winfo_pointerx() - self.window_handle.winfo_rootx()
        y = self.window_handle.winfo_pointery() - self.window_handle.winfo_rooty()
        if  self.root.winfo_x() <= x <= self.root.winfo_x() + self.root.winfo_width() and self.root.winfo_y() <= y <= self.root.winfo_y() + self.root.winfo_height():
            return True
        return False
