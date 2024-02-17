from tkinter import Button

from seynax.ui.core.components.components import Component
from seynax.ui.core.ui_window import UIWindow

ui_window = UIWindow()
ui_window.handle.update()
c = ui_window.container()
c.component(Button, text='coucou0')
c.component(Button, text='coucou1')
c.component(Button, text='coucou2')
c.component(Button, text='coucou3')

ui_window.start()

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
