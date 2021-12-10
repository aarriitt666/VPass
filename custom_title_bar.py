from tkinter import *

root = Tk()


def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


root.overrideredirect(True)  # turns off title bar, geometry
root.geometry('1200x700+150+75')  # set new geometry

# make a frame for the title bar
title_bar = Frame(root, bg='black', relief='raised', bd=2)

# put a close button on the title bar
close_button = Button(title_bar, text='X', command=root.destroy)

# a canvas for the main area of the window
window = Canvas(root, bg='black')

title_bar.grid(ipady=2, ipadx=590)
close_button.grid(padx=1165, ipady=2, ipadx=7, sticky=E)
window.grid(sticky=W)

# bind title bar motion to the move window function
title_bar.bind('<B1-Motion>', move_window)

root.mainloop()
