from tkinter import Label, Tk, Text, Menu, Frame, Button, LEFT, BOTH, Grid, Canvas, RIGHT, N, Y

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
        sub_menu = self.add(ComponentMenu, **args)

        return sub_menu

    def cascade(self, **args):
        sub_menu = self.add(ComponentMenu, **args)

        self.menu.add_cascade(label=sub_menu.menu.cget('title'), menu=sub_menu.menu)

        return sub_menu

    def command(self, **args):
        if 'accelerator' in args and 'command' in args:
            self.window.bind_all(keyboard.translate(args['accelerator']), lambda event: args['command']())
        args['font'] = self.theme.font
        self.menu.add_command(**args)


class ComponentMenu(UIManager):
    def __init__(self, window: Tk, theme: Theme, parent = None, **args):
        super().__init__(window, theme, parent)
        self.root = self.add(Frame, width=1920, height=self.theme.font_size + 10, **args)

    def cascade(self, **args):
        menu_entry = self.add(ComponentMenuEntry, closeable=False, **args)
        self.root.pack()

        return menu_entry


class ComponentMenuEntry(UIManager):
    def __init__(self, window: Tk, theme: Theme, parent = None, closeable: bool = True, **args):
        super().__init__(window, theme, parent)
        self.closeable = closeable

        self.args = args
        self.root = Frame(self.window, width=1920, height=self.theme.font_size + 10)
        if 'text' in args:
            self.cascade(text=args['text'])
        if not self.closeable:
            self.open()
        else:
            self.close()

    def cascade(self, **args):
        menu_entry = self.add(ComponentMenuEntry)
        button = self.add(Button, command=lambda: menu_entry.open(), **args)
        button.pack(side=LEFT)
        self.close()
        return menu_entry

    def open(self):
        self.root.place(x=0, y=self.theme.font_size + 10, width=1920, height=self.theme.font_size + 10)
        self.root.pack()

        self.window.bind("<Key>",       self.key)
        self.window.bind("<Button-1>",  self.mouse)

    def close(self):
        if not self.closeable:
            return

        self.window.unbind("<Key>")
        self.window.unbind("<Button-1>")

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