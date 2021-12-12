import os.path

from cryptography.fernet import Fernet
from key_generation import KeyGen

f_key = None
new_keygen = None
master_password_is_valid = None
done_encrypting = False


class Encrypting:
    def __init__(self):
        self.master_passwd = master_password_is_valid
        self.new_keygen = new_keygen
        self.f_key = f_key
        self.done_encrypting = done_encrypting

    def encrypting(self, passwd_validity, file_path):
        global f_key
        global new_keygen
        global master_password_is_valid
        global done_encrypting
        master_password_is_valid = passwd_validity
        if master_password_is_valid:
            new_keygen = KeyGen()
            f_key = new_keygen.read_key()
            file_full_path = file_path
            if os.path.exists(file_full_path):
                with open(file_full_path, mode='r') as encrypt_a_file:
                    file_content = encrypt_a_file.read()
                encoded_file = file_content.encode()
                with open('f_file_key.key', mode='rb') as get_f_key:
                    f_key_as_token = get_f_key.read()
                f = Fernet(f_key_as_token)
                encrypted = f.encrypt(encoded_file)
                with open(file_full_path, mode='wb') as encrypted_content_to_file:
                    encrypted_content_to_file.write(encrypted)
                done_encrypting = True
            return self.done_encrypting

    def decrypting(self, passwd_validity, file_path):
        global f_key
        global new_keygen
        global master_password_is_valid
        global done_encrypting
        master_password_is_valid = passwd_validity
        if master_password_is_valid:
            new_keygen = KeyGen()
            f_key = new_keygen.read_key()
            file_full_path = file_path
            if os.path.exists(file_full_path):
                encrypted_file_path = file_full_path
                with open(encrypted_file_path, mode='rb') as read_encrypted_file:
                    encrypted_file_content = read_encrypted_file.read()
                f = Fernet(f_key)
                decrypted = f.decrypt(encrypted_file_content)
                with open(f'{encrypted_file_path}', mode='wb') as write_decrypted_to_file:
                    write_decrypted_to_file.write(decrypted)
                done_encrypting = False
            return self.done_encrypting
