from tkinter import Menu, Frame, Text, Label, Button, LEFT, RIGHT, BOTH, N, Canvas, S, W, E

from ui.core.components.components import ComponentLabel, ComponentTextBox, ComponentMenuEntry

from seynax.ui.core.ui_window import UIWindow

window = UIWindow()
menu = window.add(ComponentMenuEntry, closeable=False)
file_menu = menu.cascade(text='File', accelerator='CTRL+I')
open_menu = file_menu.cascade(text='Open')
save_menu = file_menu.cascade(text='Save')

window_menu = menu.cascade(text='Window')
theme_menu = window_menu.cascade(text='Theme')
theme_menu.cascade(text='Dark')
theme_menu.cascade(text='Light')
zoom_in_menu = window_menu.cascade(text='Zoom in', accelerator='CTRL+O')
zoom_in_menu.cascade(text='A')
zoom_in_menu.cascade(text='B')
zoom_out_menu = window_menu.cascade(text='Zoom out')
a=zoom_out_menu.cascade(text='A')
a.cascade(text='C')
a.cascade(text='D')
zoom_out_menu.cascade(text='B')
menu.open()

'''frameC = window.add(Frame, width=100, height=100)
frameC.config(background='red')
frameC.pack()
frameC.place(x=frameA.winfo_width(), y=frameA.winfo_height())'''

'''frame = window.add(Frame)
frame.grid(column=0, row=0, sticky='nsew', padx=5, pady=50)
direction = 'horizontal'
if direction == 'vertical':
    button_a = Button(frame, text='BOUTON A').grid(row=0, column=1)
    button_b = Button(frame, text='BOUTON B').grid(row=1, column=1)
    button_c = Button(frame, text='BOUTON C').grid(row=2, column=1)
    button_c = Button(frame, text='BOUTON C').grid(row=3, column=1)
elif direction == 'horizontal':
    button_a = Button(frame, text='BOUTON A').grid(row=0, column=0)
    button_b = Button(frame, text='BOUTON B').grid(row=0, column=1)
    button_c = Button(frame, text='BOUTON C').grid(row=0, column=2)
    button_c = Button(frame, text='BOUTON C').grid(row=0, column=3)'''




window.start()


'''frameC = window.add(Frame, width=100, height=100)
frameC.config(background='red')
frameC.pack()
frameC.place(x=frameA.winfo_width(), y=frameA.winfo_height())'''

'''frame = window.add(Frame)
frame.grid(column=0, row=0, sticky='nsew', padx=5, pady=50)
direction = 'horizontal'
if direction == 'vertical':
    button_a = Button(frame, text='BOUTON A').grid(row=0, column=1)
    button_b = Button(frame, text='BOUTON B').grid(row=1, column=1)
    button_c = Button(frame, text='BOUTON C').grid(row=2, column=1)
    button_c = Button(frame, text='BOUTON C').grid(row=3, column=1)
elif direction == 'horizontal':
    button_a = Button(frame, text='BOUTON A').grid(row=0, column=0)
    button_b = Button(frame, text='BOUTON B').grid(row=0, column=1)
    button_c = Button(frame, text='BOUTON C').grid(row=0, column=2)
    button_c = Button(frame, text='BOUTON C').grid(row=0, column=3)'''




window.start()
