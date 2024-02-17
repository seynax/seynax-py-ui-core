from tkinter import Tk

from seynax.ui.core.container.ui_container import UIContainer
from seynax.ui.core.ui_manager import Theme


class UIWindow(UIContainer):
    def __init__(self, width: int = 1920, height: int = 1080, name: str = '', font_size: int = 22, background: str = 'gray16', foreground: str = 'gray64'):
        self.handle = Tk()
        super().__init__(self, theme=Theme(self, font_size, background, foreground))
        self.handle.wm_title(name)
        self.handle.geometry(f'{width}x{height}')
        self.update_color()
        self.opened_menus = {}
        self.handle.bind('<Escape>', lambda event: self.close_all_menu())
        self.handle.bind('<Shift-Escape>', lambda event: self.handle.quit())

    def close_all_menu(self):
        for menu in self.opened_menus.copy().values():
            menu.close()
        self.opened_menus.clear()

    def update_color(self):
        super().update_color()
        self.handle.config(background=self.theme.background)

    def dark_mode(self):
        self.theme.set_color('gray16', 'gray64')

    def light_mode(self):
        self.theme.set_color('gray64', 'gray16')

    def start(self):
        self.handle.mainloop()
