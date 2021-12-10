from mypass_ui import UserInterface
import encrypting

valid_or_not = False


def encryption_starting():
    new_encrypting = encrypting.Encrypting()
    new_valid_or_not = valid_or_not
    new_encrypting.encrypting(passwd_validity=new_valid_or_not)


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
            encryption_starting()


if __name__ == '__main__':
    main()
