from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_encryption_key():
    return AESGCM.generate_key(bit_length=128)


def generate_aesgcm(key):
    return AESGCM(key)


def encrypt(nonce, aesgcm, data):
    ct = aesgcm.encrypt(nonce, data, None)
    return ct


def decrypt(nonce, aesgcm, encrypted_data):
    data = aesgcm.decrypt(nonce, encrypted_data, None)
    return data
