from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time

def generate_share_key():
    return get_random_bytes(32)

def encrypt_share(password, share_key, expiry_hours=24):
    expiry = int(time.time()) + (expiry_hours * 3600)
    data = f"{password}|{expiry}".encode()
    cipher = AES.new(share_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + tag + ciphertext, share_key

def decrypt_share(encrypted_data, share_key):
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(share_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag).decode()
    password, expiry = plaintext.split("|")
    if int(time.time()) > int(expiry):
        raise ValueError("Message expired")
    return password