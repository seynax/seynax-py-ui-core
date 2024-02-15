from tkinter import Tk

from seynax.ui.core.ui_manager import UIManager, Theme


class UIWindow(UIManager):
    def __init__(self, width: int = 1920, height: int = 1080, name: str = '', font_size: int = 22, background: str = 'gray16', foreground: str = 'gray64'):
        super().__init__(Tk(), Theme(self, font_size, background, foreground))
        self.window.wm_title(name)
        self.window.geometry(f'{width}x{height}')
        self.update_color()

    def update_color(self):
        super().update_color()
        self.window.config(background=self.theme.background)

    def dark_mode(self):
        self.theme.set_color('gray16', 'gray64')

    def light_mode(self):
        self.theme.set_color('gray64', 'gray16')

    def start(self):
        self.window.mainloop()
