import copy
from tkinter.font   import Font
from typing import Type, List

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
