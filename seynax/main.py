from tkinter import Menu, Frame, Text, Label

from ui.core.components.components import ComponentLabel, ComponentTextBox, ComponentMenu

from seynax.ui.core.ui_window import UIWindow

window = UIWindow()
menu = window.add(ComponentMenu)
menu.cascade(text='coucou')

window.start()
