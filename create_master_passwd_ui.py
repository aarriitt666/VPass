import os.path
import tkinter.messagebox
from tkinter import *

import encrypting
import get_hash
import key_generation
import mypass_ui

MAIN_BG = '#05132b'
MAIN_TEXT = '#2ce5e8'
MAIN_FONT = ('Courier', 14, 'normal')
SUB_FONT = ('Courier', 9, 'normal')
ENTRY_FONT = ('Courier', 14, 'italic')
BUTTON_FONT = ('Courier', 12, 'bold')
BUTTON_FONT2 = ('Courier', 11, 'bold')
ENTRY_BOXES_BG = '#ab8b82'
ENTRY_BOXES_FG = '#060d47'
BUTTON_BG = '#d4483b'
BUTTON_FG = '#ebeb0e'
BUTTON_ACTIVE_BG = '#780c1c'
BUTTON_ACTIVE_FG = '#d1d0c9'
IMPORTANT_FG = '#e3e154'
MAIN_HL_BG = '#5c350b'

valid_or_not = False
new_get_hash = None


class UserInterface(Tk):
    def __init__(self):
        super().__init__()
        self.valid_or_not = valid_or_not
        self.logins_data_existed = False
        self.title('VPass')
        self.config(bg=MAIN_BG)
        self.minsize(870, 500)
        # Variables
        self.new_get_hash = new_get_hash
        self.master_password_button_click = False
        # Removing default title bar and default geometry
        self.overrideredirect(True)  # turns off title bar, geometry
        self.geometry('870x500+150+75')  # set new geometry
        # make a frame for the title bar
        self.title_bar = Frame(self, bg='black', relief='flat', bd=2)
        self.title_bar.bind('<Map>', self.screen_appear)
        self.title_bar.bind('<Button-3>', self.show_screen)
        # Put a close button on the title bar
        self.close_button = Button(self.title_bar, text='X', command=self.closing_app, fg=BUTTON_FG, bg=BUTTON_BG,
                                   activeforeground='white', activebackground='black', highlightbackground=MAIN_HL_BG)
        # Put a minimize button on the title bar
        self.minimize_button = Button(self.title_bar, text='-', command=self.hide_screen, fg=BUTTON_FG, bg=BUTTON_BG,
                                      activeforeground='white', activebackground='black',
                                      highlightbackground=MAIN_HL_BG)
        # Grid the widgets
        self.title_bar.grid(ipady=0, ipadx=0, column=0, row=0, rowspan=16, columnspan=23, sticky=N)
        self.close_button.grid(columnspan=23, padx=840, ipady=2, ipadx=7, column=2, row=0, sticky=E)
        self.minimize_button.grid(columnspan=23, padx=810, ipady=2,
                                  ipadx=7, column=1, row=0, sticky=E)
        # Bind title bar motion to the move window function
        self.title_bar.bind('<B1-Motion>', self.move_window)
        # Canvas
        self.canvas = Canvas(width=500, height=330)
        self.canvas.grid(sticky=W, row=0, column=0, rowspan=16, columnspan=4, padx=0)
        self.logo_img = PhotoImage(file='logo_custom.png')
        self.canvas.create_image(300, 120, image=self.logo_img)
        self.canvas.config(bg=MAIN_BG, highlightthickness=0)
        # Welcome Label
        self.welcome_label = Label(text='Welcome. Please create a master password!', bg=MAIN_BG, font=MAIN_FONT,
                                   fg=MAIN_TEXT,
                                   highlightthickness=0)
        self.welcome_label.place(x=230, y=290)
        # Password Label
        self.password_label1 = Label(text='Create', bg=MAIN_BG,
                                     font=MAIN_FONT, fg=MAIN_TEXT, highlightthickness=0)
        self.password_label1.grid(sticky=E, row=6, column=0, rowspan=16, padx=25)
        self.password_label2 = Label(text='Master', bg=MAIN_BG,
                                     font=MAIN_FONT, fg=MAIN_TEXT, highlightthickness=0)
        self.password_label2.grid(sticky=E, row=7, column=0, rowspan=16, padx=25)
        self.password_label3 = Label(text='Password', bg=MAIN_BG,
                                     font=MAIN_FONT, fg=MAIN_TEXT, highlightthickness=0)
        self.password_label3.grid(sticky=E, row=8, column=0, rowspan=16, padx=25)
        # Password Entry Box
        self.password_entry_box_txt = StringVar()
        self.password_entry_box = Entry(textvariable=self.password_entry_box_txt, font=ENTRY_FONT, width=29,
                                        highlightthickness=0, bg=ENTRY_BOXES_BG, fg=ENTRY_BOXES_FG)
        self.password_entry_box.focus()
        self.password_entry_box.grid(sticky=W, row=6, column=1, rowspan=16, columnspan=23, ipady=3)
        self.password_entry_box.bind(
            '<Return>', self.add_or_change_master_password_button_click_bind)
        # Show Info Label
        self.show_important_info_label1 = Label(text='Don\'t forget', bg=MAIN_BG, font=SUB_FONT, fg=IMPORTANT_FG,
                                                highlightthickness=0)
        self.show_important_info_label1.place(x=610, y=340)
        self.show_important_info_label2 = Label(text='your master password!', bg=MAIN_BG, font=SUB_FONT,
                                                fg=IMPORTANT_FG,
                                                highlightthickness=0)
        self.show_important_info_label2.place(x=580, y=360)
        # tkinter.messagebox.showinfo('showinfo', 'Don\'t forget your master password!')
        # Save Button
        add_button_txt = StringVar()
        self.add_button = Button(textvariable=add_button_txt, width=49, font=BUTTON_FONT, highlightthickness=3, bd=0,
                                 bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                 activeforeground=BUTTON_ACTIVE_FG,
                                 command=self.add_or_change_master_password_button_click)
        self.add_button.grid(sticky=W, row=8, column=1, rowspan=16, columnspan=23, pady=400)
        add_button_txt.set('Save')

        # Back to main app Button
        self.back_to_vpass_button_txt = StringVar()
        self.back_to_vpass_button = Button(textvariable=self.back_to_vpass_button_txt, width=15, font=BUTTON_FONT,
                                           highlightthickness=3, bd=0,
                                           bg=MAIN_BG, activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                           activeforeground=BUTTON_ACTIVE_FG, command=self.back_to_vpass_app_wins)
        self.back_to_vpass_button_txt.set('Back to Vpass')
        self.back_to_vpass_button.place(x=630, y=70)

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

    def add_or_change_master_password_button_click_bind(self, event):
        self.add_or_change_master_password_button_click()

    def add_or_change_master_password_button_click(self):
        self.master_password_button_click = True
        self.add_or_change_master_password()
        return self.master_password_button_click

    def add_or_change_master_password(self):
        global new_get_hash
        if self.master_password_button_click is True:
            get_user_master_passwd = self.password_entry_box.get()
            new_get_hash = get_hash.GetHash()
            new_get_hash.let_us_hash_it(password=get_user_master_passwd)
            new_key_gen = key_generation.KeyGen()
            new_key_gen.automate_key_generation_using_password_and_salt(
                user_password=get_user_master_passwd)
            if new_get_hash.hash_it_has_it:
                self.password_entry_box_txt.set('')
                question_result = tkinter.messagebox.askquestion(
                    'Do you want to return to the main application?')
                if question_result == 'yes':
                    self.destroy()
                    mypass_ui.UserInterface()
                else:
                    self.destroy()
                    UserInterface()

    def back_to_vpass_app_wins(self):
        self.destroy()
        mypass_ui.UserInterface()

    def encryption_starting(self):
        new_encrypting = encrypting.Encrypting()
        new_valid_or_not = self.valid_or_not
        new_encrypting.encrypting(passwd_validity=new_valid_or_not)

    def decryption_starting(self):
        new_decrypting = encrypting.Encrypting()
        new_valid_or_not = self.valid_or_not
        new_decrypting.decrypting(passwd_validity=new_valid_or_not)

    def closing_app(self):
        if self.valid_or_not is True:
            self.encryption_starting()
        self.destroy()

    def login_data_exist(self):
        if os.path.exists('logins_data.csv'):
            self.logins_data_existed = True
            return self.logins_data_existed


def main():
    UserInterface()
    mainloop()


if __name__ == '__main__':
    main()
