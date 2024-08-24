from cryptography.fernet import Fernet


def generate_encryption_key():
    return Fernet.generate_key()


def generate_cipher_suite(key):
    return Fernet(key)


def encrypt(cipher_suite, data):
    return cipher_suite.encrypt(data)


def decrypt(cipher_suite, encrypted_data):
    return cipher_suite.decrypt(encrypted_data)
