import bcrypt
import bcrypt as b
import time
import _cffi_backend


hash_it_has_it = True

class GetHash:
    """
    This should be used only once to get a hash so this hash could be stored in a database or in a file.  Protected
    database is recommended because it's an added layer of protection/security.  Regardless, password will be hashed
    after using this class's function let_us_hash_it().
    """

    def __init__(self):
        self.hash = None
        self.new_passwd = None
        self.hash_done = None
        self.hash_it_has_it = hash_it_has_it

    def let_us_hash_it(self, password):
        global hash_it_has_it
        self.new_passwd = password.encode()
        self.hash = bcrypt.hashpw(self.new_passwd, b.gensalt())
        with open('b_file_hash.txt', mode='wb') as b_file_hash:
            b_file_hash.write(self.hash)
        return hash_it_has_it

    def check_hash(self, password):
        passwd = password.encode()
        try:
            with open('b_file_hash.txt', mode='rb') as open_hash_file:
                self.hash_done = open_hash_file.read()
        except FileNotFoundError:
            pass
        else:
            if b.checkpw(passwd, self.hash_done):
                return True
            else:
                return False

    def main(self):
        prog_runs = True
        while prog_runs:
            chk_hash_input = input(
                f'Do you want to compare your password with your hash?  Type \'y\' for yes \'n\' for no. >>').lower()
            if chk_hash_input == 'y':
                your_passwd_input = input(f'What is your password? >>  ')
                result = self.check_hash(your_passwd_input)
                if result is True:
                    print('Your password is valid!')
                    prog_runs = False
                else:
                    print('This isn\'t your password!')
                    sleep_time = 10
                    print(f'The program will exit in {sleep_time} seconds.')
                    for i in range(1, sleep_time + 1):
                        print(i)
                        time.sleep(1)
                    break

            elif chk_hash_input == 'n':
                pass
            user_input = input(
                'Do you want to get your password hashed?  Type \'y\' for yes \'n\' for no. >>  ').lower()
            if user_input == 'y':
                user_password = input(f'What is your password? >>')
                self.let_us_hash_it(user_password)
                prog_runs = False
            elif user_input == 'n':
                sleep_time = 10
                print(f'The program will exit in {sleep_time} seconds.')
                for i in range(1, sleep_time + 1):
                    print(i)
                    time.sleep(1)
                prog_runs = False


if __name__ == '__main__':
    start_hashing = GetHash()
    start_hashing.main()
