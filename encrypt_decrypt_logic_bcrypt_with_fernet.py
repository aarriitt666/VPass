from cryptography.fernet import Fernet
from key_generation import KeyGen
from get_hash import GetHash
import time

new_keygen = KeyGen()
new_gethash = GetHash()
user_input = input(f'What is your password?')
hash_truth = new_gethash.check_hash(password=user_input)
if hash_truth is True:
    f_key = new_keygen.read_key()
    new_user_input = input(f'Do you want to encrypt a file? Type \'y\' for yes \'n\' for no. >>').lower()
    if new_user_input == 'y':
        file_full_path = input(f'Please enter a file full path: >>  ')

        # Here we should write code to sanitize path of file and check validity.  Short of time, I coudn't put the
        # effort to do just this.  This will have to be done at another time.

        with open(file_full_path, mode='r') as encrypt_a_file:
            file_content = encrypt_a_file.read()
        encoded_file = file_content.encode()
        with open('f_file_key.key', mode='rb') as get_f_key:
            f_key_as_token = get_f_key.read()
        f = Fernet(f_key_as_token)
        encrypted = f.encrypt(encoded_file)
        with open(file_full_path, mode='wb') as encrypted_content_to_file:
            encrypted_content_to_file.write(encrypted)
        print(f'Now you can open up your {file_full_path} to see that regular content is now encrypted!')
    elif new_user_input == 'n':
        new_user_input = input(
            'Do you want to decrypt a file instead? Type \'y\' for yes and \'n\' for no.  >>  ').lower()
        if new_user_input == 'y':
            need_passwd = input('Please enter your password! >>  ')
            new_hash_truth = new_gethash.check_hash(need_passwd)
            if new_hash_truth is True:
                f_key = new_keygen.read_key()
                encrypted_file_path = input(f'Please enter a file\'s full path!')
                with open(encrypted_file_path, mode='rb') as read_encrypted_file:
                    encrypted_file_content = read_encrypted_file.read()
                f = Fernet(f_key)
                decrypted = f.decrypt(encrypted_file_content)
                with open(f'{encrypted_file_path}', mode='wb') as write_decrypted_to_file:
                    write_decrypted_to_file.write(decrypted)
                    print(f'Your file at {encrypted_file_path} is now decrypted!')
        else:
            print('The program is now exiting in 10 seconds!')
            sleep_time = 10
            print(f'The program will exit in {sleep_time} seconds.')
            for i in range(1, sleep_time + 1):
                print(i)
                time.sleep(1)
                exit()
else:
    print('Your password is not valid!  The program will exit in 10 seconds.')
    sleep_time = 10
    for i in range(1, sleep_time + 1):
        print(i)
        time.sleep(1)
    exit()
