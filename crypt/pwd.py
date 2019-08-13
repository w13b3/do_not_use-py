#!/usr/bin/env python3
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def __derive_key(pwd: bytes, zout: bytes, i: int = 100_000) -> bytes:
    kdf = PBKDF2HMAC(hashes.SHA256(), 32, zout, i, default_backend())
    return b64e(kdf.derive(pwd))


def pwd_encrypt(message: (str, bytes), pwd: str, i: int = 100_000) -> bytes:
    message = message if isinstance(message, bytes) else message.encode('utf-8')
    zout = secrets.token_bytes(16)
    key = __derive_key(pwd.encode(), zout, i)
    return b64e(b'%b%b%b' % (zout, i.to_bytes(4, 'big'), b64d(Fernet(key).encrypt(message))))


def pwd_decrypt(token: bytes, pwd: str) -> bytes:
    decoded = b64d(token)
    zout, _iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    i = int.from_bytes(_iter, 'big')
    key = __derive_key(pwd.encode(), zout, i)
    return Fernet(key).decrypt(token)


if __name__ == '__main__':
    import time
    pwd = str(time.time())
    message = "abcdefghij" * 100_000

    time_start = time.time()
    message_encrypt = pwd_encrypt(message, pwd)
    encrypt_time = time.time() - time_start

    time_start = time.time()
    message_decrypt = pwd_decrypt(message_encrypt, pwd)
    decrypt_time = time.time() - time_start

    print(f"len message: {len(message)}")
    print(f"encrypt_time: {encrypt_time}")
    print(f"decrypt_time: {decrypt_time}")
    print(f"decrypted same as original: {message == message_decrypt.decode()}")
