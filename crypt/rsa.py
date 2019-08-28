#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rsa.py

import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature, InvalidKey


def __assure_private_key(private_key: rsa) -> None:
    """
    Check if a private key is a private key
    :param private_key: rsa  the private key to check
    :raises InvalidKey: if given key is invalid
    :return: None
    """
    private_keys = (
        rsa.RSAPrivateKey, rsa.RSAPrivateNumbers, rsa.RSAPrivateKeyWithSerialization)
    if not isinstance(private_key, private_keys):
        raise InvalidKey("Given key is not a private key")


def __assure_public_key(public_key: rsa) -> None:
    """
    Check if a public key is a public key
    :param public_key: rsa  the public key to check
    :raises InvalidKey: if given key is invalid
    :return: None
    """
    public_keys = (
        rsa.RSAPublicKey, rsa.RSAPublicNumbers, rsa.RSAPublicKeyWithSerialization)
    if not isinstance(public_key, public_keys):
        raise InvalidKey("Given key is not a public key")


def get_private_key(public_exponent: int = 65537, key_size: int = 4096) -> rsa:
    """
    Private helper function to generate a private key
    :param public_exponent:  int
    :param key_size:  int
    :return:  rsa  private key
    """
    private_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
            backend=default_backend())
    return private_key


def get_public_pem(public_key: rsa) -> bytes:
    """
    Private function to make generate a pem which can be saved to store the public key
    :param public_key:  the public key made from a private key
    :return:  bytes
    """
    __assure_public_key(public_key)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pem


def get_private_pem(private_key: rsa, pwd: bytes = None) -> bytes:
    """
    Private function to make generate a pem which can be saved to store the private key
    :param private_key:  the private_key
    :param pwd: password: if not None, Best available encryption is chosen
                and the private key is encrypted with a the password
    :return:  bytes
    """
    __assure_private_key(private_key)
    encrypt_algo = serialization.NoEncryption()
    if bool(pwd):  # if password and length is greater of equal to 1.
        encrypt_algo = serialization.BestAvailableEncryption(pwd)

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encrypt_algo)
    return pem


def generate_keys(directory: str, pwd: bytes = None) -> (rsa.RSAPrivateKey, rsa.RSAPublicKey):
    """
    Generate the public and private keys
    Generated keys have a default name, you should rename them
    This can be done with os.rename()
    :param directory: folder where the keys are made
                      overwrite the existing keys
    :param pwd: password: if not None, Best available encryption is chosen
                and the private key is encrypted with a the password
    :return: private, public keys
    """
    private_key = generate_private_key(directory, pwd)
    public_key = generate_public_key(directory, private_key)
    return private_key, public_key


def generate_private_key(directory: str, pwd: bytes = None) -> rsa.RSAPrivateKey:
    """
    Generate the private key, this key should not be shared with anyone!
    Generated keys have a default name, you should rename them
    This can be done with os.rename()
    :param directory: folder where the keys are made
                      overwrite the existing keys
    :param pwd: password: if not None, Best available encryption is chosen
    :return: rsa  private key object
    """
    directory = os.path.realpath(directory)
    if not os.path.isdir(directory):
        directory = os.path.dirname(directory)

    # generate private key
    private_key = get_private_key()

    private_path = os.path.join(directory, './private_key.pem')
    with open(private_path, 'wb') as open_file:
        private_pem = get_private_pem(private_key, pwd)
        open_file.write(private_pem)
    return private_key


def generate_public_key(directory: str, private_key: rsa) -> rsa.RSAPublicKey:
    """
    Generate the public key, share this key with anyone
    Generated keys have a default name, you should rename them
    This can be done with os.rename()
    :param directory: folder where the keys are made
                      overwrite the existing keys
    :raises InvalidKey: if given key is invalid
    :return: rsa  private key object
    """
    __assure_private_key(private_key)
    public_key = private_key.public_key()
    public_path = os.path.join(directory, './public_key.pem')
    with open(public_path, 'wb') as open_file:
        public_pem = get_public_pem(public_key)
        open_file.write(public_pem)
    return public_key


def read_private_key(key_file: str, pwd: bytes = None) -> rsa.RSAPrivateKey:
    """
    Read and return a private key
    To use with an incoming encrypted message
    :param key_file: str  path to the keyfile
    :param pwd: bytes  if the private key is locked with an password
    :raises FileNotFoundError:  if key_file doesnt exist
    :return: serialization object
    """
    key_file = os.path.realpath(key_file)
    if not os.path.exists(key_file):
        raise FileNotFoundError("given file doesnt exist: {0}".format(key_file))
    with open(key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=pwd, backend=default_backend())
    return private_key


def read_public_key(key_file: str) -> rsa.RSAPublicKey:
    """
    Read and return a public key
    To use with encrypting an outgoing message
    :param key_file: str
    :raises FileNotFoundError:  if key_file doesnt exist
    :return: serialization object
    """
    key_file = os.path.realpath(key_file)
    if not os.path.exists(key_file):
        raise FileNotFoundError("given file doesnt exist: {0}".format(key_file))
    with open(key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend())
    return public_key


def sign_message(message: bytes, private_key: rsa) -> bytes:
    """
    Sign a message with a private key
    This is done to make sure the message to send comes from the right source
    :param message: bytes
    :param private_key: rsa
    :raises InvalidKey: if given key is invalid
    :return: bytes
    """
    __assure_private_key(private_key)
    signature = private_key.sign(
        message, padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256())
    return signature


def verify_signed_message(signature: bytes, message: bytes, public_key: rsa) -> bool:
    """
    Verify the incoming message with a public key
    This to ensure the incoming message is indeed from the expected source
    :param signature: received signature
    :param message: incoming message
    :param public_key: a public key from the source of the message
    :raises InvalidKey: if given key is invalid
    :return: bool
    """
    __assure_public_key(public_key)
    try:
        public_key.verify(signature, message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())
    except InvalidSignature:
        return False
    else:
        return True


def rsa_encrypt(message: bytes, public_key: rsa) -> bytes:
    """
    Encrypt a message with a public key
    :param message:  byte string to encrypt
    :param public_key:  key to encrypt the message with
    :raises InvalidKey: if given key is invalid
    :return: bytes  as the encrypted message
    """
    __assure_public_key(public_key)
    encrypted_message = public_key.encrypt(
        message, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))
    return encrypted_message


def rsa_decrypt(encrypted: bytes, private_key: rsa) -> bytes:
    """
    Decrypt an encrypted message with a private key
    :param encrypted:  byte string encrypted message
    :param private_key:  key to decrypt the message with
    :raises InvalidKey: if given key is invalid
    :return: bytes  as the decrypted message
    """
    __assure_private_key(private_key)
    decrypted_message = private_key.decrypt(
        encrypted, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))
    return decrypted_message


if __name__ == '__main__':
    from time import time
    from tempfile import TemporaryDirectory

    original_message = b'Hello'
    print(f"original message: {original_message}")
    pwd = bytes(str(time()), 'ascii')  # pwd is the current time
    directory = TemporaryDirectory()  # create tempdir
    private_path = os.path.join(directory.name, 'private_key.pem')
    public_path = os.path.join(directory.name, 'public_key.pem')

    # generate_keys(directory.name, pwd)  # generate the keys
    private_key1 = generate_private_key(directory.name, pwd)
    private_key2 = get_private_key()  # use hidden method for testing
    public_key1 = generate_public_key(directory.name, private_key1)
    public_key2 = private_key1.public_key()
    public_key3 = private_key2.public_key()

    # read saved keys
    # private_key = read_private_key(private_path, pwd)
    # public_key = read_public_key(public_path)  # read the keys

    # keys are objects
    # print(f"private_key1: {private_key1}")
    # print(f"private_key2: {private_key2}")
    # print(f"public_key1: {public_key1}")
    # print(f"public_key2: {public_key2}")
    # print(f"public_key2: {public_key3}")

    # verify all keys are different
    print(f"public_key1 == public_key2 -> {public_key1 == public_key2}")
    print(f"public_key1 == public_key3 -> {public_key1 == public_key3}")
    print(f"public_key2 == public_key3 -> {public_key2 == public_key3}")

    # encrypt and decrypt message
    encrypted_message = rsa_encrypt(original_message, public_key1)
    print(f"encrypted_message: {encrypted_message}")  # long byte string
    decrypted_message = rsa_decrypt(encrypted_message, private_key1)
    print(f"decrypted_message: {decrypted_message}")  # b'hello'
    print(f"original_message == decrypted_message -> {original_message == decrypted_message}")

    # check if signed message can only be verified by public keys derived from the private key
    # which the signed message was signed with
    signature = sign_message(encrypted_message, private_key1)
    # public_key1 & public_key2 is made by private_key1
    public1_verify = verify_signed_message(signature, encrypted_message, public_key1)
    public2_verify = verify_signed_message(signature, encrypted_message, public_key2)
    # public_key3 is made by private_key2
    public3_verify = verify_signed_message(signature, encrypted_message, public_key3)

    print(f"signature signed with private_key1: {signature}")
    print(f"public_key1 verify: {public1_verify}")
    print(f"public_key2 verify: {public2_verify}")
    print(f"public_key3 verify: {public3_verify}")

    directory.cleanup()  # delete tempdir
