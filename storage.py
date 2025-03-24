import sqlite3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

class PasswordStorage:
    def __init__(self, db_path="passwords.db"):
        self.db_path = db_path
        self.key = self.load_or_create_key()
        self.setup_db()

    def load_or_create_key(self):
        key_file = "master_key.bin"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        key = get_random_bytes(32)
        with open(key_file, "wb") as f:
            f.write(key)
        return key

    def setup_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                         (id INTEGER PRIMARY KEY, alias TEXT, password BLOB)''')
        conn.commit()
        conn.close()

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return nonce + tag + ciphertext

    def decrypt(self, data):
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()

    def add_password(self, alias, password):
        encrypted = self.encrypt(password)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (alias, password) VALUES (?, ?)", (alias, encrypted))
        conn.commit()
        conn.close()

    def get_password(self, alias):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM passwords WHERE alias = ?", (alias,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return self.decrypt(result[0])
        return None