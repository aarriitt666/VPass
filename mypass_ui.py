import csv
import os.path
import string
from tkinter import *
from csv import *
from tkinter import messagebox
import random as r

import cryptography.fernet

from password_notebook_ui import PasswordNotebook
import generate_passwd
import create_master_passwd_ui
import get_hash
import encrypting
import json

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

valid_or_not = False
json_new_data = None


class UserInterface(Tk):
    def __init__(self):
        super().__init__()
        self.valid_or_not = valid_or_not
        self.logins_data_existed = False
        self.title('VPass')
        self.config(bg=MAIN_BG)
        self.minsize(870, 500)
        # Variables
        self.new_website = None
        self.new_email_or_username = None
        self.new_password = None
        self.new_password_notebook = None
        self.new_passwd = None
        self.new_create_master_passwd_ui = None
        self.reset_val = False
        self.w = None
        self.eu = None
        self.pw = None
        self.data = None
        self.new_data = json_new_data
        # Removing default title bar and default geometry
        self.overrideredirect(True)  # turns off title bar, geometry
        self.geometry('870x500+150+75')  # set new geometry
        # make a frame for the title bar
        self.title_bar = Frame(self, bg='black', relief='flat', bd=2)
        self.title_bar.bind('<Map>', self.screen_appear)
        self.title_bar.bind('<Button-3>', self.show_screen)
        # Put a close button on the title bar
        self.close_button = Button(self.title_bar, text='X', fg=BUTTON_FG, bg=BUTTON_BG,
                                   activeforeground='white', activebackground='black', highlightbackground=MAIN_HL_BG,
                                   command=self.closing_app)
        # Put a minimize button on the title bar
        self.minimize_button = Button(self.title_bar, text='-', command=self.hide_screen, fg=BUTTON_FG, bg=BUTTON_BG,
                                      activeforeground='white', activebackground='black',
                                      highlightbackground=MAIN_HL_BG)
        # Grid the widgets
        self.title_bar.grid(ipady=0, ipadx=0, column=0, row=0, rowspan=16, columnspan=23, sticky=N)
        self.close_button.grid(columnspan=23, padx=840, ipady=2, ipadx=7, column=2, row=0, sticky=E)
        self.minimize_button.grid(columnspan=23, padx=810, ipady=2, ipadx=7, column=1, row=0, sticky=E)
        # Bind title bar motion to the move window function
        self.title_bar.bind('<B1-Motion>', self.move_window)
        # Canvas
        self.canvas = Canvas(width=500, height=250)
        self.canvas.grid(sticky=W, row=0, column=0, rowspan=16, columnspan=4, padx=0)
        self.logo_img = PhotoImage(file='C:/Users/argda/PycharmProjects/password-manager/logo_custom.png')
        self.canvas.create_image(300, 120, image=self.logo_img)
        self.canvas.config(bg=MAIN_BG, highlightthickness=0)
        # Password Notebook Button
        password_notebook_button_txt = StringVar()
        self.password_notebook_button = Button(textvariable=password_notebook_button_txt, width=18,
                                               font=BUTTON_FONT, highlightthickness=3, bd=0,
                                               bg='#05132b', activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                               activeforeground=BUTTON_ACTIVE_FG, command=self.open_password_notebook)
        self.password_notebook_button.grid(sticky=W, row=2, rowspan=10, column=1, columnspan=23, pady=0, padx=0)
        password_notebook_button_txt.set('Password Notebook')
        # Menu font seperator
        self.menu_font_seperator = Label(text='|', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT,
                                         highlightthickness=0)
        self.menu_font_seperator.grid(sticky=W, row=2, column=2, rowspan=10, columnspan=23, pady=0, padx=120)
        # Add/Change Master Password Button
        add_change_master_passwd_button_txt = StringVar()
        self.add_change_master_passwd_button = Button(textvariable=add_change_master_passwd_button_txt, width=27,
                                                      font=BUTTON_FONT, highlightthickness=3, bd=0,
                                                      bg='#05132b', activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                                      activeforeground=BUTTON_ACTIVE_FG,
                                                      command=self.open_create_master_passwd_ui)
        self.add_change_master_passwd_button.grid(sticky=W, row=2, column=3, rowspan=10, columnspan=23, pady=0, padx=70)
        add_change_master_passwd_button_txt.set('Add/Change Master Password')
        # Website Entry Box Label
        self.website_entry_box_label = Label(text='Website', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT,
                                             highlightthickness=0)
        self.website_entry_box_label.grid(sticky=E, row=7, column=0, rowspan=12, padx=25)
        # Website Entry Box
        self.website_entry_box_txt = StringVar()
        self.website_entry_box = Entry(textvariable=self.website_entry_box_txt, font=ENTRY_FONT, width=42,
                                       highlightthickness=0, bg=ENTRY_BOXES_BG, fg=ENTRY_BOXES_FG)
        self.website_entry_box.focus()
        self.website_entry_box.grid(sticky=W, row=7, column=1, rowspan=12, columnspan=23, ipady=3)
        self.website_entry_box.bind('<Return>', self.get_login_details_bind)
        # Email/Username Entry Box Label
        self.email_username_entry_box_label = Label(text='Email/Username', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT,
                                                    highlightthickness=0)
        self.email_username_entry_box_label.grid(sticky=E, row=8, column=0, rowspan=12, padx=25)
        # Email/Username Entry Box
        self.email_username_entry_txt = StringVar()
        self.email_username_entry_box = Entry(textvariable=self.email_username_entry_txt, font=ENTRY_FONT, width=42,
                                              highlightthickness=0, bg=ENTRY_BOXES_BG, fg=ENTRY_BOXES_FG)
        self.email_username_entry_box.grid(sticky=W, row=8, column=1, rowspan=12, columnspan=23, ipady=3)
        self.email_username_entry_box.bind('<Return>', self.get_login_details_bind)
        # Password Label
        self.password_label = Label(text='Password', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT, highlightthickness=0)
        self.password_label.grid(sticky=E, row=9, column=0, rowspan=12, padx=25)
        # Password Entry Box
        self.password_entry_box_txt = StringVar()
        self.password_entry_box = Entry(textvariable=self.password_entry_box_txt, font=ENTRY_FONT, width=25,
                                        highlightthickness=0, bg=ENTRY_BOXES_BG, fg=ENTRY_BOXES_FG)
        self.password_entry_box.grid(sticky=W, row=9, column=1, rowspan=12, columnspan=23, ipady=3)
        self.password_entry_box.bind('<Return>', self.get_login_details_bind)
        # Generate Password Button
        self.generate_password_button_txt = StringVar()
        self.generate_password_button = Button(textvariable=self.generate_password_button_txt, width=19,
                                               font=BUTTON_FONT2,
                                               highlightthickness=3, bd=0, bg=BUTTON_BG,
                                               activebackground=BUTTON_ACTIVE_BG,
                                               fg=BUTTON_FG, activeforeground=BUTTON_ACTIVE_FG,
                                               command=self.generate_password)
        self.generate_password_button.grid(sticky=W, row=9, column=4, rowspan=12, columnspan=23, padx=67)
        self.generate_password_button_txt.set('Generate Password')
        # Add Button
        add_button_txt = StringVar()
        self.add_button = Button(textvariable=add_button_txt, width=46, font=BUTTON_FONT, highlightthickness=2, bd=0,
                                 bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                 activeforeground=BUTTON_ACTIVE_FG, command=self.get_login_details)
        self.add_button.grid(sticky=W, row=10, column=1, rowspan=12, columnspan=23, pady=430)
        add_button_txt.set('Add')

        # Master Password Unlock Entry Box
        self.master_passwd_entry_box_txt = StringVar()
        self.master_passwd_entry_box = Entry(textvariable=self.master_passwd_entry_box_txt, font=ENTRY_FONT, width=25,
                                             highlightthickness=0, bg=ENTRY_BOXES_BG, fg=ENTRY_BOXES_FG, show='*')
        self.master_passwd_entry_box.place(x=450, y=200)
        self.master_passwd_entry_box.bind('<Return>', self.chk_master_passwd_bind)
        # Enter Master Password Button
        self.master_passwd_button_txt = StringVar()
        self.master_passwd_button = Button(textvariable=self.master_passwd_button_txt, width=27, font=BUTTON_FONT,
                                           highlightthickness=2, bd=0,
                                           bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                           activeforeground=BUTTON_ACTIVE_FG, command=self.check_master_password)
        self.master_passwd_button.place(x=450, y=230)
        self.master_passwd_button_txt.set('Enter Your Master Password')

        # Reset Button
        self.reset_button_txt = StringVar()
        self.reset_button = Button(textvariable=self.reset_button_txt, width=8, font=BUTTON_FONT,
                                   highlightthickness=2, bd=0,
                                   bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                   activeforeground=BUTTON_ACTIVE_FG, command=self.reset)
        self.reset_button_txt.set('Reset')
        self.reset_button.place(x=30, y=60)

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

    def login_info_to_file_json(self, website, email_or_username, password):
        global json_new_data
        self.w = website
        self.eu = email_or_username
        new_password = [i.replace(',', r.choice(string.punctuation)) for i in str(password)]
        temp_p = ''.join(new_password)
        new_password1 = [i.replace('"', r.choice(string.punctuation)) for i in str(temp_p)]
        temp_p1 = ''.join(new_password1)
        self.pw = temp_p1.strip(' "\t\r\n')
        json_new_data = {
            self.w: {
                'email_or_username': self.eu,
                'password': self.pw
            }
        }

        try:
            with open('logins_data_json.json', mode='r') as f:
                self.data = json.load(f)
                self.data.update(json_new_data)
            with open('logins_data_json.json', mode='w') as f:
                json.dump(self.data, f, indent=4)
        except FileNotFoundError:
            with open('logins_data_json.json', mode='w') as f:
                json.dump(json_new_data, f, indent=4)

    def login_info_to_file(self, website, email_or_username, password):
        self.new_website = website
        self.new_email_or_username = email_or_username
        new_password = [i.replace(',', r.choice(string.punctuation)) for i in str(password)]
        temp_p = ''.join(new_password)
        new_password1 = [i.replace('"', r.choice(string.punctuation)) for i in str(temp_p)]
        self.new_password = ''.join(new_password1)
        row = [self.new_website, self.new_email_or_username, self.new_password]
        new_row = [i.strip(' "\t\r\n') for i in row]
        with open('logins_data.csv', mode='a', newline='',
                  encoding='utf-8') as f:
            append = writer(f, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
            append.writerow(new_row)

    def get_login_details_bind(self, event):
        self.get_login_details()

    def get_login_details(self):
        if not self.valid_or_not:
            messagebox.showinfo('Return', 'You must enter a master password to add logins.')
            self.destroy()
            UserInterface()
        else:
            website_login = self.website_entry_box_txt.get()
            email_username = self.email_username_entry_txt.get()
            password_info = self.password_entry_box_txt.get()
            if len(website_login) == 0 or len(email_username) == 0 or len(password_info) == 0:
                messagebox.showinfo('Return', 'This field cannot be empty!')
            else:
                self.login_info_to_file(website=website_login, email_or_username=email_username, password=password_info)
                self.login_info_to_file_json(website=website_login, email_or_username=email_username,
                                             password=password_info)
                self.website_entry_box_txt.set('')
                self.email_username_entry_txt.set('')
                self.password_entry_box_txt.set('')

    def open_password_notebook(self):
        if self.valid_or_not is True:
            self.destroy()
            self.new_password_notebook = PasswordNotebook()
            self.new_password_notebook.display_logins_only()
            self.new_password_notebook.valid_or_not = self.valid_or_not
        else:
            messagebox.showinfo('Return', 'You need to enter a correct master password in the main application '
                                          'before you can proceed to change your master password.')

    def generate_password(self):
        if not self.valid_or_not:
            messagebox.showinfo('Return', 'You must enter a master password to use this feature!')
        else:
            self.destroy()
            generate_passwd.GeneratePasswd()

    def chk_master_passwd_bind(self, event):
        self.check_master_password()

    def check_master_password(self):
        global valid_or_not
        master_passwd = self.master_passwd_entry_box.get()
        new_get_hash = get_hash.GetHash()
        valid_or_not = new_get_hash.check_hash(password=master_passwd)
        self.valid_or_not = valid_or_not
        if self.valid_or_not:
            try:
                self.decryption_starting()
            except (cryptography.fernet.InvalidToken, TypeError):
                with open('vpass_error_log.txt', mode='a') as f:
                    custom_error_msg = 'In check_master_password function of mypass_ui.py, an error raises about ' \
                                       'Fernet InvalidToken when trying to decrypt using decryption_starting ' \
                                       'function.  Also, TypeError may be raised if the content isn\'t a byte ' \
                                       ' type.'
                    f.write(custom_error_msg)
                self.master_passwd_entry_box_txt.set('')
                self.destroy()
                UserInterface()
            else:
                self.master_passwd_entry_box_txt.set('')
                messagebox.showinfo('Return', 'You have successfully enter a master password!')
        else:
            messagebox.showinfo('Return',
                                'Incorrect master password, without valid master password, your encrypted '
                                'database won\'t be accessible to you as it\'s still encrypted.')

    def open_create_master_passwd_ui(self):
        if not os.path.exists(
                'b_file_hash.txt') or self.valid_or_not is True:
            self.destroy()
            self.new_create_master_passwd_ui = create_master_passwd_ui.UserInterface()
            self.new_create_master_passwd_ui.valid_or_not = self.valid_or_not
            self.new_create_master_passwd_ui.add_or_change_master_password()
        else:
            messagebox.showinfo('Return', 'You need to enter a correct master password in the main application '
                                          'before you can proceed to change your master password.')

    def reset(self):
        question_res = messagebox.askquestion('Erase data and master password?  Proceed????????????')
        if question_res == 'yes':
            if os.path.exists('logins_data.csv'):
                os.remove('logins_data.csv')
            if os.path.exists('b_file_hash.txt'):
                os.remove('b_file_hash.txt')
            if os.path.exists('f_file_key.key'):
                os.remove('f_file_key.key')
            if os.path.exists('vpass_error_log.txt'):
                os.remove('vpass_error_log.txt')
            if os.path.exists('logins_data_json.json'):
                os.remove('logins_data_json.json')
            self.reset_val = True
            self.destroy()
            UserInterface()

        else:
            messagebox.showinfo('Return')
        return self.reset_val

    def encryption_starting(self):
        new_encrypting = encrypting.Encrypting()
        new_valid_or_not = self.valid_or_not
        new_encrypting.encrypting(passwd_validity=new_valid_or_not, file_path='logins_data.csv')
        new_encrypting.encrypting(passwd_validity=new_valid_or_not, file_path='logins_data_json.json')

    def decryption_starting(self):
        new_decrypting = encrypting.Encrypting()
        new_valid_or_not = self.valid_or_not
        new_decrypting.decrypting(passwd_validity=new_valid_or_not, file_path='logins_data.csv')
        new_decrypting.decrypting(passwd_validity=new_valid_or_not, file_path='logins_data_json.json')

    def closing_app(self):
        if self.valid_or_not is True:
            try:
                self.encryption_starting()
            except (cryptography.fernet.InvalidToken, TypeError):
                with open('vpass_error_log.txt', mode='a') as f:
                    custom_error_msg = 'In closing_app function of mypass_ui.py, an error raises about ' \
                                       'Fernet InvalidToken when trying to encrypt using encryption_starting ' \
                                       'function.  Also, TypeError may be raised if the content isn\'t a byte ' \
                                       ' type.'
                    f.write(custom_error_msg)
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
