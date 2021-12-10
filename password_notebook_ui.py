import os.path
from tkinter import *
from tkinter import messagebox
import pandas as pd
from edit_logins import EditLoginsUi
import mypass_ui
import encrypting
import create_master_passwd_ui

MAIN_BG = '#05132b'
MAIN_TEXT = '#2ce5e8'
MAIN_FONT = ('Courier', 14, 'normal')
ENTRY_FONT = ('Courier', 14, 'italic')
BUTTON_FONT = ('Courier', 12, 'bold')
BUTTON_FONT2 = ('Courier', 11, 'bold')
ENTRY_BOXES_BG = '#05132b'
ENTRY_BOXES_FG = '#999395'
BUTTON_FG = '#ebeb0e'
SUB_BUTTON_FG = '#b03115'
BUTTON_BG = '#5c3116'
BUTTON_ACTIVE_BG = '#780c1c'
BUTTON_ACTIVE_FG = '#d1d0c9'
MAIN_HL_BG = '#5c350b'
MAIN_TEXT_BG = '#3b0d0d'
LIST_BOX_SELECT_FG = '#827b2e'
LIST_BOX_SELECT_BG = '#071326'


class PasswordNotebook(Tk):
    def __init__(self):
        super().__init__()
        self.valid_or_not = None
        self.logins_data_existed = False
        self.title('VPass Notebook')
        self.config(bg=MAIN_BG)
        self.minsize(1200, 700)
        self.x = None
        self.y = None
        # Variables
        self.login_details_df = None
        self.sb = None
        self.logins = None
        self.selected_login = None
        self.new_create_master_passwd_ui = None
        # Removing default title bar and default geometry
        self.overrideredirect(True)  # turns off title bar, geometry
        self.geometry('1200x700+150+75')  # set new geometry
        # make a frame for the title bar
        self.title_bar = Frame(self, bg='black', relief='flat', bd=2)
        self.title_bar.bind('<Map>', self.screen_appear)
        self.title_bar.bind('<Button-3>', self.show_screen)
        # Put a close button on the title bar
        self.close_button = Button(self.title_bar, text='X', command=self.closing_app, fg=BUTTON_FG, bg='#d4483b',
                                   activeforeground='white', activebackground='black', highlightbackground=MAIN_HL_BG)
        # Put a minimize button on the title bar
        self.minimize_button = Button(self.title_bar, text='-', command=self.hide_screen, fg=BUTTON_FG, bg='#d4483b',
                                      activeforeground='white', activebackground='black',
                                      highlightbackground=MAIN_HL_BG)
        # Grid the widgets
        self.title_bar.grid(ipady=2, ipadx=800, column=0, row=0, columnspan=2, sticky=N)
        self.close_button.grid(columnspan=2, rowspan=4, padx=1170, ipady=2, ipadx=7, column=2, row=0, sticky=E)
        self.minimize_button.grid(columnspan=2, rowspan=4, padx=1140, ipady=2, ipadx=7, column=1, row=0, sticky=E)
        # Bind title bar motion to the move window function
        self.title_bar.bind('<B1-Motion>', self.move_window)
        # Left Frame
        self.left_frame = Frame(bd=5, highlightthickness=0, bg=MAIN_BG)
        self.left_frame.grid(row=1, column=0, rowspan=4, columnspan=2, sticky=W)
        # Canvas
        self.canvas = Canvas(self.left_frame, width=360, height=60)
        self.canvas.grid(row=1, column=0, sticky=W)
        self.logo_img = PhotoImage(file='C:/Users/argda/PycharmProjects/password-manager/logo_custom_small.png')
        self.canvas.create_image(25, 25, image=self.logo_img)
        self.canvas.config(bg=MAIN_BG, highlightthickness=0)
        # Canvas
        self.canvas2 = Canvas(self.left_frame, width=810, height=60)
        self.canvas2.grid(row=1, column=1, sticky=E)
        self.canvas2.config(bg=MAIN_BG, highlightthickness=0)
        # Edit Logins
        edit_logins_button_txt = StringVar()
        self.edit_logins_button = Button(self.left_frame, textvariable=edit_logins_button_txt, width=12,
                                         font=BUTTON_FONT, highlightthickness=3, bd=0,
                                         bg=MAIN_BG, activebackground=BUTTON_ACTIVE_BG, fg=SUB_BUTTON_FG,
                                         activeforeground=BUTTON_ACTIVE_FG, command=self.edit_logins)
        self.edit_logins_button.grid(row=1, column=1, sticky=W, padx=192)
        edit_logins_button_txt.set('Edit Logins')
        # Menu font seperator 1
        self.menu_font_seperator1 = Label(self.left_frame, text='|', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT,
                                          highlightthickness=0)
        self.menu_font_seperator1.grid(row=1, column=1, sticky=W, padx=323)
        # Add New Logins
        new_logins_button_txt = StringVar()
        self.new_logins_button = Button(self.left_frame, textvariable=new_logins_button_txt, width=16,
                                        font=BUTTON_FONT, highlightthickness=3, bd=0,
                                        bg=MAIN_BG, activebackground=BUTTON_ACTIVE_BG, fg=SUB_BUTTON_FG,
                                        activeforeground=BUTTON_ACTIVE_FG, command=self.open_mypass_ui)
        self.new_logins_button.grid(row=1, column=1, sticky=E, padx=300)
        new_logins_button_txt.set('Add New Logins')
        # Menu font seperator 2
        self.menu_font_seperator2 = Label(self.left_frame, text='|', bg=MAIN_BG, font=MAIN_FONT, fg=MAIN_TEXT,
                                          highlightthickness=0)
        self.menu_font_seperator2.grid(row=1, column=1, sticky=E, padx=283)
        # Add/Change Master Password Button
        add_change_master_passwd_button_txt = StringVar()
        self.add_change_master_passwd_button = Button(self.left_frame, textvariable=add_change_master_passwd_button_txt,
                                                      width=27,
                                                      font=BUTTON_FONT, highlightthickness=3, bd=0,
                                                      bg=MAIN_BG, activebackground=BUTTON_ACTIVE_BG, fg=SUB_BUTTON_FG,
                                                      activeforeground=BUTTON_ACTIVE_FG,
                                                      command=self.open_create_master_passwd_ui)
        self.add_change_master_passwd_button.grid(column=1, row=1, sticky=E, padx=0, ipadx=2)
        add_change_master_passwd_button_txt.set('Add/Change Master Password')
        # List Box
        self.list_logins = Listbox(self.left_frame, height=26, width=30, bg=ENTRY_BOXES_BG,
                                   highlightbackground=MAIN_HL_BG, highlightthickness=1,
                                   bd=0, fg=ENTRY_BOXES_FG, font=ENTRY_FONT, selectforeground=LIST_BOX_SELECT_FG,
                                   selectbackground=LIST_BOX_SELECT_BG, selectmode=SINGLE)
        self.list_logins.grid(rowspan=4, columnspan=2, row=3, column=0, padx=2, pady=2, ipadx=10, sticky=W)
        # Calling display_logins_only function to get the list of logins
        logins_list = self.display_logins_only()
        if logins_list is not None:
            for item in logins_list:
                self.list_logins.insert(logins_list.index(item), item)
            self.list_logins.bind("<<ListboxSelect>>", self.list_logins_used)
        # Info Box Text
        self.info_box = Text(self.left_frame, height=27, width=75, highlightthickness=1, bd=0, fg=ENTRY_BOXES_FG,
                             font=ENTRY_FONT, bg=MAIN_TEXT_BG, highlightbackground=MAIN_HL_BG, wrap='word')
        self.info_box.focus()
        self.info_box.grid(row=3, column=1, rowspan=4, columnspan=2, sticky=E)
        # # Scrollbar for Info Box
        # self.sb = Scrollbar(self.left_frame, orient='vertical')
        # self.sb.grid(sticky=NS, row=3, column=2, rowspan=4)
        # self.info_box.config(yscrollcommand=self.sb.set)
        # self.sb.config(command=self.info_box.yview)

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

    def read_login_details(self):
        if os.path.exists('logins_data.csv'):
            new_data = pd.read_csv('logins_data.csv', names=['Logins', 'Email or Username', 'Password'])
            self.login_details_df = pd.DataFrame(new_data)
            return self.login_details_df

    def display_logins_only(self):
        if os.path.exists('logins_data.csv'):
            new_data = pd.read_csv('logins_data.csv', names=['Logins', 'Email or Username', 'Password'])
            self.logins = new_data.Logins.to_list()
            return self.logins

    def display_login_value(self):
        if os.path.exists('logins_data.csv'):
            new_data = pd.read_csv('logins_data.csv', names=['Logins', 'Email or Username', 'Password'])
            df = pd.DataFrame(new_data)
            new_df = df[df.Logins == self.selected_login]
            set_index_column = new_df.set_index('Logins')
            new_df = set_index_column.rename(columns={'Logins': '', 'Email or Username': '', 'Password': ''})
            result = new_df.to_csv(header=False)
            new_result = result.replace(',', ' | ')
            self.info_box.delete('1.0', END)
            self.info_box.insert('1.0',
                                 'Known bugs for editing logins:  1) Double quotes in password can create issues such'
                                 ' as unwanted double quotes could get multiply in the password string. 2) Trying to '
                                 'edit a login but trying to generate password more than once results in logins info '
                                 'return as None or empty in the entry fields.\n'
                                 'New feature added:  1) Whenever you use automated generate password feature, you can'
                                 ' just do Ctrl+V keys to paste the password into a website.\n'
                                 'Please report more bugs to me at my email address or call me up.  Only people who '
                                 'know me personally can do this.  If you don\'t know me personally, '
                                 'you might have to wait for me to discover more bugs on my own and fix \'em bugs.\n'
                                 '-- Note from Vinh Nguyen.\n')
            self.info_box.insert(END, '-------------------------------------------------------------------------\n')
            self.info_box.insert(END,
                                 'Logins' + ' ' + '-' + ' ' + 'Email/Username' + ' ' + '-' + ' ' + 'Password' + '\n')
            self.info_box.insert(END, '-------------------------------------------------------------------------')
            self.info_box.insert(END, '\n' + new_result)

    def list_logins_used(self, event):
        # Gets current selection from list_logins
        self.selected_login = self.list_logins.get(self.list_logins.curselection())
        self.display_login_value()

    def edit_logins(self):
        msgbox = messagebox.askquestion(title='Edit Logins Confirmation',
                                        message=f'Do you want to edit {self.selected_login}?')
        if msgbox == 'yes':
            if self.selected_login:
                # Close current window
                self.destroy()
                # Open up Edit Logins Ui
                new_edit_logins = EditLoginsUi()
                new_edit_logins.valid_or_not = self.valid_or_not
                # Reading in data from stored logins data file using Pandas
                if os.path.exists('logins_data.csv'):
                    new_data = pd.read_csv('logins_data.csv', names=['Logins', 'Email or Username', 'Password'])
                    # Move data into DataFrame for easy manipulation
                    df = pd.DataFrame(new_data)
                    # Get a selected row of data
                    new_df = df[df.Logins == self.selected_login]
                    # Set custom index column to remove default extra sequential index column
                    set_index_col = new_df.set_index('Logins')
                    # At this point we can select a specific column value in the row.
                    get_email_username_col = set_index_col['Email or Username']
                    get_password_col = set_index_col['Password']
                    # Renaming the row's header with empty space
                    get_email_username_col.rename({'Email or Username': ''})
                    get_password_col.rename({'Password': ''})
                    # Dropping the Index column altogether
                    get_email_username_col.reset_index(drop=True, inplace=True)
                    get_password_col.reset_index(drop=True, inplace=True)
                    # Removing the header altogether
                    email_username_result = get_email_username_col.to_csv(header=False)
                    password_result = get_password_col.to_csv(header=False)
                    # Replacing the default index dropped value which is '0, with empty space
                    new_email_username_result = email_username_result.replace('0,', '')
                    new_password_result = password_result.replace('0,', '')
                    # Insert clean data value into Edit Logins Ui Form Fields.
                    new_edit_logins.website_entry_box_txt.set(self.selected_login)
                    new_edit_logins.email_username_entry_txt.set(new_email_username_result)
                    new_edit_logins.password_entry_box_txt.set(new_password_result)
                    new_edit_logins.selected_login = self.selected_login
            else:
                messagebox.showinfo('Return', 'You must select a logins to edit.')
        else:
            messagebox.showinfo('Return')

    def open_mypass_ui(self):
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
        if self.valid_or_not:
            self.encryption_starting()
        self.destroy()

    def login_data_exist(self):
        if os.path.exists('logins_data.csv'):
            self.logins_data_existed = True
            return self.logins_data_existed

    def open_create_master_passwd_ui(self):
        if not os.path.exists('b_file_hash.txt') or self.valid_or_not is True:
            self.destroy()
            self.new_create_master_passwd_ui = create_master_passwd_ui.UserInterface()
            self.new_create_master_passwd_ui.valid_or_not = self.valid_or_not
            self.new_create_master_passwd_ui.add_or_change_master_password()
        else:
            messagebox.showinfo('Return', 'You need to enter a correct master password in the main application '
                                          'before you can proceed to change your master password.')


def main():
    PasswordNotebook()
    mainloop()


if __name__ == '__main__':
    main()
