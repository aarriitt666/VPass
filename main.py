import cryptography.fernet

from mypass_ui import UserInterface
import encrypting

valid_or_not = False


def encryption_starting():
    new_encrypting = encrypting.Encrypting()
    new_valid_or_not = valid_or_not
    new_encrypting.encrypting(passwd_validity=new_valid_or_not, file_path='logins_data.csv')
    new_encrypting.encrypting(passwd_validity=new_valid_or_not, file_path='logins_data_json.json')


def main():
    global valid_or_not
    try:
        mypass_ui = UserInterface()
        mypass_ui.mainloop()
        valid_or_not = mypass_ui.valid_or_not
    except ValueError:
        print('Error: there was an error.')
    except ZeroDivisionError:
        print('Error: 0 is an invalid number.')
    except Exception:
        print('Error: another unknown error occurred.')
        if valid_or_not:
            try:
                encryption_starting()
            except (cryptography.fernet.InvalidToken, TypeError):
                with open('vpass_error_log.txt', mode='a') as f:
                    custom_error_msg = 'In main() function of main.py, an error raises about ' \
                                       'Fernet InvalidToken when trying to encrypt using encryption_starting ' \
                                       'function.  Also, TypeError may be raised if the content isn\'t a byte ' \
                                       ' type.'
                    f.write(custom_error_msg)


if __name__ == '__main__':
    main()
