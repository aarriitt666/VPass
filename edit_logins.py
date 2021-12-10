import csv
from tkinter import messagebox
import create_master_passwd_ui
from tkinter import *
import pandas as pd
from csv import *
import password_notebook_ui
import generate_passwd_for_edit_logins
import os.path
import encrypting

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

new_selected_login = None
new_condition = None
gen_passwd_boolean_val = False
valid_or_not = False


class EditLoginsUi(Tk):
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
        self.selected_login = None
        self.new_password_notebook_ui = None
        self.new_mod_csv_data = None
        self.new_gen_passwd = None
        self.new_selected_login = new_selected_login
        self.gen_passwd_boolean_val = gen_passwd_boolean_val
        self.new_master_passwd_ui = None
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
                                                      command=self.open_master_password_ui)
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
        self.website_entry_box.bind('<Return>', self.edit_login_in_file_bind)
        # Email/Username Entry Box Label
        self.email_username_entry_box_label = Label(text='Email/Username', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT,
                                                    highlightthickness=0)
        self.email_username_entry_box_label.grid(sticky=E, row=8, column=0, rowspan=12, padx=25)
        # Email/Username Entry Box
        self.email_username_entry_txt = StringVar()
        self.email_username_entry_box = Entry(textvariable=self.email_username_entry_txt, font=ENTRY_FONT, width=42,
                                              highlightthickness=0, bg=ENTRY_BOXES_BG, fg=ENTRY_BOXES_FG)
        self.email_username_entry_box.grid(sticky=W, row=8, column=1, rowspan=12, columnspan=23, ipady=3)
        self.email_username_entry_box.bind('<Return>', self.edit_login_in_file_bind)
        # Password Label
        self.password_label = Label(text='Password', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT, highlightthickness=0)
        self.password_label.grid(sticky=E, row=9, column=0, rowspan=12, padx=25)
        # Password Entry Box
        self.password_entry_box_txt = StringVar()
        self.password_entry_box = Entry(textvariable=self.password_entry_box_txt, font=ENTRY_FONT, width=25,
                                        highlightthickness=0, bg=ENTRY_BOXES_BG, fg=ENTRY_BOXES_FG)
        self.password_entry_box.grid(sticky=W, row=9, column=1, rowspan=12, columnspan=23, ipady=3)
        self.password_entry_box.bind('<Return>', self.edit_login_in_file_bind)
        # Generate Password Button
        generate_password_button_txt = StringVar()
        self.generate_password_button = Button(textvariable=generate_password_button_txt, width=19, font=BUTTON_FONT2,
                                               highlightthickness=3, bd=0, bg=BUTTON_BG,
                                               activebackground=BUTTON_ACTIVE_BG,
                                               fg=BUTTON_FG, activeforeground=BUTTON_ACTIVE_FG,
                                               command=self.gen_random_passwd)
        self.generate_password_button.grid(sticky=W, row=9, column=4, rowspan=12, columnspan=23, padx=67)
        generate_password_button_txt.set('Generate Password')
        # Save Button
        add_button_txt = StringVar()
        self.add_button = Button(textvariable=add_button_txt, width=22, font=BUTTON_FONT, highlightthickness=2, bd=0,
                                 bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                 activeforeground=BUTTON_ACTIVE_FG, command=self.edit_login_in_file)
        self.add_button.grid(sticky=W, row=10, column=1, rowspan=12, columnspan=23, pady=430)
        add_button_txt.set('Save')

        # Delete Button
        delete_button_txt = StringVar()
        self.delete_button = Button(textvariable=delete_button_txt, width=22, font=BUTTON_FONT, highlightthickness=2,
                                    bd=0,
                                    bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg=BUTTON_FG,
                                    activeforeground=BUTTON_ACTIVE_FG, command=self.delete_login)
        self.delete_button.place(x=520, y=430)
        delete_button_txt.set('Delete')

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

    def edit_login_in_file_bind(self, event):
        self.edit_login_in_file()

    def edit_login_in_file(self):
        global new_condition
        if os.path.exists('logins_data.csv'):
            new_data = pd.read_csv('logins_data.csv', names=['Logins', 'Email or Username', 'Password'])
            df = pd.DataFrame(new_data)
            index = df.index
            if gen_passwd_boolean_val is True:
                new_condition = df[
                                    'Logins'] == self.new_selected_login  # work with using generated password button
            else:
                new_condition = df['Logins'] == self.selected_login  # work without using generated password button
            selected_login_indices = index[new_condition]
            selected_login_indices_list = selected_login_indices.to_list()
            new_data_drop = new_data.drop(selected_login_indices_list[0])
            new_csv_data = new_data_drop.to_csv(index=False, header=False, line_terminator='\r\n')
            new_csv_data = new_csv_data.strip('"')
            with open('logins_data.csv', mode='w', newline='', encoding='utf-8') as modify_logins_data:
                modify_logins_data.write(new_csv_data)
            self.get_login_details()

    def delete_login(self):
        if os.path.exists('logins_data.csv'):
            new_data = pd.read_csv('logins_data.csv', names=['Logins', 'Email or Username', 'Password'])
            df = pd.DataFrame(new_data)
            index = df.index
            condition = df['Logins'] == self.selected_login
            selected_login_indices = index[condition]
            selected_login_indices_list = selected_login_indices.to_list()
            new_data_drop = new_data.drop(selected_login_indices_list[0])
            new_csv_data = new_data_drop.to_csv(index=False, header=False)
            with open('logins_data.csv', mode='w', newline='', encoding='utf-8') as modify_logins_data:
                modify_logins_data.write(new_csv_data)
            self.website_entry_box_txt.set('')
            self.email_username_entry_txt.set('')
            self.password_entry_box_txt.set('')

    def login_info_to_file(self, website, email_or_username, password):
        self.new_website = website
        self.new_email_or_username = email_or_username
        self.new_password = password
        row = [self.new_website, self.new_email_or_username, self.new_password]
        print(row)
        new_row = [i.strip(' "\t\r\n') for i in row]
        print(new_row)
        with open('logins_data.csv', mode='a',
                  encoding='utf-8') as f:
            append = writer(f, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
            append.writerow(new_row)

    def get_login_details(self):
        website_login = self.website_entry_box_txt.get()
        email_username = self.email_username_entry_txt.get()
        password_info = self.password_entry_box_txt.get()
        if len(website_login) == 0 or len(email_username) == 0 or len(password_info) == 0:
            messagebox.showinfo('Return', 'You must enter some information before you can add or save data.')
        else:
            self.login_info_to_file(website=website_login, email_or_username=email_username, password=password_info)
            self.website_entry_box_txt.set('')
            self.email_username_entry_txt.set('')
            self.password_entry_box_txt.set('')

    def open_password_notebook(self):
        self.destroy()
        self.new_password_notebook_ui = password_notebook_ui.PasswordNotebook()
        self.new_password_notebook_ui.valid_or_not = self.valid_or_not

    def gen_random_passwd(self):
        global gen_passwd_boolean_val
        global new_selected_login
        new_selected_login = self.selected_login
        self.destroy()
        new_gen_passwd_for_edit = generate_passwd_for_edit_logins.GeneratePasswd()
        gen_passwd_boolean_val = new_gen_passwd_for_edit.generate_passwd_for_edit_logins_boolean

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

    def open_master_password_ui(self):
        self.destroy()
        self.new_master_passwd_ui = create_master_passwd_ui.UserInterface()


def main():
    EditLoginsUi()
    mainloop()


if __name__ == '__main__':
    main()
