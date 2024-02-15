from tkinter import Menu, Frame, Text, Label, Button, LEFT, RIGHT, BOTH

from ui.core.components.components import ComponentLabel, ComponentTextBox, ComponentMenu

from seynax.ui.core.ui_window import UIWindow

window = UIWindow()
menu = window.add(ComponentMenu)
file_menu0 = menu.cascade(text='File')
file_menu1 = menu.cascade(text='File2')
file_menu0.cascade(text='coucou0')
file_menu1.cascade(text='coucou1')

window.start()
