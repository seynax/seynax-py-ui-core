from tkinter import Label, Tk, Text, Menu, Frame, Button, LEFT, BOTH, Grid, Canvas, RIGHT, N, Y, TOP, NW, W

from utils.attributes import dict_utils

from seynax.ui.core.keyboard import keyboard
from seynax.ui.core.ui_manager import UIManager, Theme


class ComponentLabel(UIManager):
    def __init__(self, window: Tk, theme: Theme, parent = None, **args):
        super().__init__(window, theme, parent)
        self.label = self.add(Label, **args)

    def update_text(self, text: str = ''):
        self.label.config(text=text)


class ComponentTextBox(UIManager):
    def __init__(self, window: Tk, theme: Theme, text: str = '', parent = None, **args):
        super().__init__(window, theme, parent)
        self.text = text
        self.box = self.add(Text, **args)
        self.box.insert('end', text)

    def clear(self):
        self.box.delete(1.0, 'end')

    def set(self, text: str = ''):
        self.clear()
        self.box.insert('end', text)


class ComponentNativeMenu(UIManager):
    def __init__(self, window: Tk, theme: Theme, parent = None, **args):
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
            self.window.bind_all(keyboard.translate(args['accelerator']), lambda event: args['command']())
        args['font'] = self.theme.font
        self.menu.add_command(**args)


class ComponentMenuEntry(UIManager):
    def __init__(self, window: Tk, theme: Theme, parent = None, closeable: bool = True, **args):
        super().__init__(window, theme, parent)
        self.closeable = closeable

        self.args = args
        self.root = Frame(self.window, height=self.theme.font_size)
        self.root.config(background='white')
        self.direction='bottom'
        self.menu_current = None

        if 'text' in args:
            self.menu_parent = self.cascade(text=args['text'])
        else:
            self.menu_parent = None

        if not self.closeable:
            self.open()
        else:
            self.close()

    def cascade(self, **args):
        menu_entry = self.add(ComponentMenuEntry)
        button = self.add(Button, command=lambda: menu_entry.open(), **args)
        if self.menu_parent is not None:
            menu_entry.direction = 'right'
        button.pack(side=LEFT, fill=BOTH)
        menu_entry.menu_parent = button
        self.menu_current = button
        self.close()
        return menu_entry

    def menu_root_y(self):
        y = 0
        if isinstance(self.parent, ComponentMenuEntry):
            y += self.parent.menu_root_y()
        if hasattr(self, 'menu_parent') and self.menu_parent is not None:
            y += self.menu_parent.winfo_y()
        return y

    def menu_root_x(self):
        x = 0
        if isinstance(self.parent, ComponentMenuEntry):
            x += self.parent.menu_root_x()
        if hasattr(self, 'menu_parent') and self.menu_parent is not None:
            x += self.menu_parent.winfo_x()
        return x

    def menu_root_height(self):
        height = 0
        if isinstance(self.parent, ComponentMenuEntry):
            height += self.parent.menu_root_height()
        if hasattr(self, 'menu_parent') and self.menu_parent is not None:
            height += self.menu_parent.winfo_height()
        return height

    def menu_root_width(self):
        width = 0
        if isinstance(self.parent, ComponentMenuEntry):
            width += self.parent.menu_root_width()
        if hasattr(self, 'menu_parent') and self.menu_parent is not None:
            width += self.menu_parent.winfo_width()
        return width

    def open(self):
        width = 1920
        if self.menu_parent is not None:
            width = self.menu_parent.winfo_width()
            self.menu_current.pack(expand=True)
        self.root.config(background='white')
        #if self.direction == 'bottom':
        self.root.place(x=self.menu_root_x(), y=self.menu_root_height(), width=width)
        #if self.direction == 'right':
        #    self.root.place(x=self.menu_root_x()+self.parent.menu_parent.winfo_width(), y=self.menu_root_y() + self.parent.menu_parent.winfo_height(), width=width)

        self.window.bind("<Key>",       self.key)
        self.window.bind("<Button-1>",  self.mouse)

    def close(self):
        if not self.closeable:
            return

        self.window.unbind("<Key>")
        self.window.unbind("<Button-1>")

        self.root.place_forget()
        self.root.pack_forget()

    def key(self, event):
        print("pressed", repr(event.char))

    def mouse(self, event):
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
        if  self.root.winfo_x() <= x <= self.root.winfo_x() + self.root.winfo_width() and self.root.winfo_y() <= y <= self.root.winfo_y() + self.root.winfo_height():
            pass
        else:
            self.close()