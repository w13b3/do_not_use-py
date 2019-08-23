#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rsa.py

import os

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


def generate_keys(directory: str, pwd: bytes = None) -> None:
    """
    Generate the public and private keys
    Generated keys have a default name, you should rename them
    this can be done with os.rename()
    :param directory: folder where the keys are made
                      overwrite the existing keys
    :param pwd: password: if not None, Best available encryption is chosen
                and the private key is encrypted with a the password
    :return: None
    """
    directory = os.path.realpath(directory)
    if not os.path.isdir(directory):
        directory = os.path.dirname(directory)

    # generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend())

    encrypt_algo = serialization.NoEncryption()
    if bool(pwd):  # if password and length is greater of equal to 1.
        encrypt_algo = serialization.BestAvailableEncryption(pwd)

    # Store the private key
    private_path = os.path.join(directory, './private_key.pem')
    with open(private_path, 'wb') as open_file:
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encrypt_algo)
        open_file.write(pem)

    # store the public key
    public_key = private_key.public_key()
    public_path = os.path.join(directory, './public_key.pem')
    with open(public_path, 'wb') as open_file:
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        open_file.write(pem)


def read_private_key(key_file: str, pwd: bytes = None) -> rsa:
    """
    Read and return a private key
    to use with an incoming encrypted message
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


def read_public_key(key_file: str) -> rsa:
    """
    Read and return a public key
    to use with encrypting an outgoing message
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


def rsa_encrypt(message: bytes, public_key: rsa) -> bytes:
    """
    Encrypt a message with a public key
    :param message:  byte string to encrypt
    :param public_key:  key to encrypt the message with
    :return: bytes  as the encrypted message
    """
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
    :return: bytes  as the decrypted message
    """
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

    generate_keys(directory.name, pwd)  # generate the keys
    private_key = read_private_key(private_path, pwd)
    public_key = read_public_key(public_path)  # read the keys
    print(f"private_key: {private_key}")
    print(f"public_key: {public_key}")  # both are objects

    encrypted_message = rsa_encrypt(original_message, public_key)
    print(f"encrypted_message: {encrypted_message}")  # long byte string
    decrypted_message = rsa_decrypt(encrypted_message, private_key)
    print(f"decrypted_message: {decrypted_message}")  # b'hello'
    print(f"original_message == decrypted_message -> {original_message == decrypted_message}")

    directory.cleanup()  # delete tempdir
