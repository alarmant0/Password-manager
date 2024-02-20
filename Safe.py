import os
from cryptography.fernet import Fernet


class Safe:

    def __init__(self):
        self.MANAGER_PATH = os.path.join(os.getenv('APPDATA'), 'password_manager')
        self.KEY_FILE = os.path.join(os.getenv('APPDATA'), 'password_manager', 'key.key')
        self.PASSWORDS_FILE = os.path.join(os.getenv('APPDATA'), 'password_manager', 'passwords', 'pass.pass')
        self.create_path()
        self.key = self.load_or_generate_key()

    def create_path(self):
        if not os.path.exists(os.path.dirname(self.KEY_FILE)):
            os.makedirs(os.path.dirname(self.KEY_FILE))
            os.makedirs(os.path.dirname(self.PASSWORDS_FILE))

    def load_or_generate_key(self):
        if os.path.exists(self.KEY_FILE):
            with open(self.KEY_FILE, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.KEY_FILE, 'wb') as key_file:
                key_file.write(key)
            return key

    def save_pass(self, service, username, password):
        cipher = Fernet(self.key)
        encrypted_password = cipher.encrypt(password.encode()).decode()
        with open(self.PASSWORDS_FILE, 'a') as f:
            f.write(f'{service}:{username}:{encrypted_password}\n')

    def get_passwords(self):
        if os.path.exists(self.PASSWORDS_FILE):
            with open(self.PASSWORDS_FILE, 'r') as f:
                lines = f.readlines()
            return [line.strip() for line in lines]
        else:
            return []

    def decrypt(self, encrypted_password):
        cipher = Fernet(self.key)
        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        return decrypted_password

#David Pinheiro
