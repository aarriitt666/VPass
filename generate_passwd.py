from tkinter import *
import string
import random as r
import mypass_ui
import pyperclip

MAIN_BG = '#05132b'
MAIN_TEXT = '#2ce5e8'
MAIN_FONT = ('Courier', 14, 'normal')
ENTRY_FONT = ('Courier', 14, 'italic')
BUTTON_FONT = ('Courier', 12, 'bold')
BUTTON_FONT2 = ('Courier', 11, 'bold')
ENTRY_BOXES_BG = '#ab8b82'
ENTRY_BOXES_FG = '#060d47'
BUTTON_BG = '#d4483b'
BUTTON_FG = '#ebeb0e'
BUTTON_ACTIVE_BG = '#780c1c'
BUTTON_ACTIVE_FG = '#d1d0c9'
MAIN_HL_BG = '#5c350b'


class GeneratePasswd(Tk):
    def __init__(self):
        super().__init__()
        self.config(bg=MAIN_BG)
        self.title('Vpass - Generate a Password')
        self.minsize(600, 200)
        # Variables
        self.hard_to_guess_gen_passwd = None
        self.new_mypass_ui = None
        # Removing default title bar and default geometry
        self.overrideredirect(True)  # turns off title bar, geometry
        self.geometry('600x200+150+75')  # set new geometry
        # make a frame for the title bar
        self.title_bar = Frame(self, bg='black', relief='flat', bd=2)
        self.title_bar.bind('<Map>', self.screen_appear)
        self.title_bar.bind('<Button-3>', self.show_screen)
        # Put a close button on the title bar
        self.close_button = Button(self.title_bar, text='X', fg=BUTTON_FG, bg=BUTTON_BG,
                                   activeforeground='white', activebackground='black', highlightbackground=MAIN_HL_BG,
                                   command=self.reopen_mypass_ui)
        # Put a minimize button on the title bar
        self.minimize_button = Button(self.title_bar, text='-', command=self.hide_screen, fg=BUTTON_FG, bg=BUTTON_BG,
                                      activeforeground='white', activebackground='black',
                                      highlightbackground=MAIN_HL_BG)
        # Grid the widgets
        self.title_bar.grid(ipady=0, ipadx=0, column=0, row=0, rowspan=5, columnspan=5, sticky=N)
        self.close_button.grid(columnspan=5, padx=510, ipady=2, ipadx=7, column=2, row=0, sticky=E)
        self.minimize_button.grid(columnspan=5, padx=539, ipady=2, ipadx=7, column=1, row=0, sticky=E)
        # Bind title bar motion to the move window function
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.canvas = Canvas(bd=0, bg=MAIN_BG, width=450, height=200, highlightthickness=0)
        self.canvas.grid(columnspan=5, sticky=W, padx=25, rowspan=3)
        self.label = Label(self.canvas, text='Password Length', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT)
        self.label.grid(row=1, column=0, sticky=W, padx=20, rowspan=3)
        self.slider1 = Scale(self.canvas, from_=6, to=60, orient=HORIZONTAL, tickinterval=3, length=300, bg='#0d3b47',
                             fg='#8c630f', highlightthickness=0, activebackground='#7a0101', troughcolor=MAIN_BG,
                             command=self.generating_random_passwd)
        self.slider1.grid(row=1, column=1, sticky=W, columnspan=5, pady=50, rowspan=3)

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    def hide_screen(self):
        self.overrideredirect(False)
        self.iconify()

    def show_screen(self):
        self.deiconify()
        self.overrideredirect(True)

    def screen_appear(self, event):
        self.overrideredirect(True)

    def generating_random_passwd(self, *args):
        passwd_length = self.slider1.get()
        characters = string.ascii_letters + string.digits + string.punctuation
        temp = ''.join(r.choice(characters) for i in range(passwd_length))
        new_temp = temp.strip(' "\'\t\r\n')
        new_temp1 = new_temp.replace('"', '')
        self.hard_to_guess_gen_passwd = new_temp1.replace(',', '')
        return self.hard_to_guess_gen_passwd

    def reopen_mypass_ui(self):
        self.destroy()
        self.new_mypass_ui = mypass_ui.UserInterface()
        self.new_mypass_ui.new_password = self.hard_to_guess_gen_passwd
        self.new_mypass_ui.password_entry_box_txt.set(self.new_mypass_ui.new_password)
        pyperclip.copy(self.hard_to_guess_gen_passwd)


def main():
    new_gpwd = GeneratePasswd()
    new_gpwd.generating_random_passwd()
    mainloop()


if __name__ == '__main__':
    main()
