from tkinter import Label, Tk, Text, Menu, Frame, Button

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
        frame = self.add(Frame)
        self.root = frame

    def cascade(self, **args):
        button = self.add(Button)
