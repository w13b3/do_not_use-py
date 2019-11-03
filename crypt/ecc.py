#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ecc.py

import os
import logging
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature, InvalidKey


def __assure_private_key(private_key: ec) -> None:
    """
    Check if a private key is a private key
    :param private_key: ec  the private key to check
    :raises InvalidKey: if given key is invalid
    :return: None
    """
    private_keys = (
        ec.EllipticCurvePrivateKey, ec.EllipticCurvePrivateNumbers, ec.EllipticCurvePrivateNumbers)
    if not isinstance(private_key, private_keys):
        raise InvalidKey("Given key is not a private key")


def __assure_public_key(public_key: ec) -> None:
    """
    Check if a public key is a public key
    :param public_key: ec  the public key to check
    :raises InvalidKey: if given key is invalid
    :return: None
    """
    public_keys = (
        ec.EllipticCurvePublicKey, ec.EllipticCurvePublicNumbers, ec.EllipticCurvePublicKeyWithSerialization)
    if not isinstance(public_key, public_keys):
        raise InvalidKey("Given key is not a public key")


def get_private_key(curve: str = 'SECP521R1') -> ec.EllipticCurvePrivateKey:
    """
    Helper function to generate a private key
    :param curve  str  name of the function in cryptography.hazmat.primitives.asymmetric.ec
        website: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#elliptic-curves
    :type curve: str
    :return:  a new private key
    :rtype: ec.EllipticCurvePrivateKey
    """
    private_key = ec.generate_private_key(
            curve=getattr(ec, str(curve)),
            backend=default_backend())
    return private_key


def get_public_key(private_key: ec.EllipticCurvePrivateKey) -> ec.EllipticCurvePublicKey:
    """
    Helper function to generate a public key
    :param private_key: private key to get the public key from
    :type private_key: ec.EllipticCurvePrivateKey
    :return: public key
    :rtype: ec.EllipticCurvePublicKey
    """
    __assure_private_key(private_key)
    return private_key.public_key()


def get_shared_key(private_key: ec.EllipticCurvePrivateKey, peer_public_key: ec.EllipticCurvePublicKey,
                   algorithm: ec.ECDH = None) -> bytes:
    """
    creates a shared key
    mostly used ot get the derived key

    :param private_key: a private key
    :type private_key:  ec.EllipticCurvePrivateKey
    :param peer_public_key: the public key of the other party
    :type: ec.EllipticCurvePublicKey
    :param algorithm: an algoritm agreed upon with the other party
    :type algorithm: ec.ECDH
    :return:
    :rtype: bytes
    """
    __assure_private_key(private_key)
    __assure_public_key(peer_public_key)
    if not bool(algorithm) and algorithm is None:
        algorithm = ec.ECDH()
    shared_key = private_key.exchange(algorithm=algorithm, peer_public_key=peer_public_key)
    return shared_key


def get_derived_key(shared_key: bytes, data: bytes = None,
                    lenght: int = 32, salt: int = None,
                    algorithm: hashes = None) -> bytes:
    """
    Creates a derived key
    A common key between a server and client

    :param shared_key: key received from the other party
    :type shared_key: bytes
    :param data: data to include in the derived key
    :type data: bytes
    :param lenght: lenght of the key
    :type lenght: int
    :param salt: iterations used
    :type salt: int
    :param algorithm: type of algorithm that was used to create the public key
    :type algorithm: cryptography.hazmat.primitives.hashes
    :return:
    """
    if not bool(algorithm):
        algorithm = hashes.SHA256()

    derived_key = HKDF(algorithm=algorithm,
                       length=lenght,
                       salt=salt,
                       info=data,
                       backend=default_backend())
    return derived_key.derive(shared_key)


def encrypt_with_derived_key(unencrypted_data: bytes, derived_key: bytes) -> bytes:
    """
    Encrypt messages with the derived key

    :param derived_key: key received from  get_derived_key  function
    :type derived_key: bytes
    :param unencrypted_data: data to encrypt
    :type unencrypted_data: bytes
    :return: encrypted data
    :rtype: bytes
    """
    key = derived_key.zfill(12)
    nonce, secret = (key[:6] + key[-6:]), key[::-1][0:12]
    chacha = ChaCha20Poly1305(derived_key)
    encrypted_data = chacha.encrypt(nonce, unencrypted_data, derived_key)
    return encrypted_data


def decrypt_with_derived_key(encrypted_data: bytes, derived_key: bytes) -> bytes:
    """
    Decrypt messages with the derived key

    :param derived_key: key received from  get_derived_key  function
    :type derived_key: bytes
    :param encrypted_data: encrypted data from the  encrypt_with_derived_key  function
    :type encrypted_data: bytes
    :return: decrypted data
    :rtype: bytes
    """
    key = derived_key.zfill(12)
    nonce, secret = (key[:6] + key[-6:]), key[::-1][0:12]
    chacha = ChaCha20Poly1305(derived_key)
    unencrypted_data = chacha.decrypt(nonce, encrypted_data, derived_key)
    return unencrypted_data


def generate_public_pem(public_key: ec.EllipticCurvePublicKey) -> bytes:
    """
    Generates a Privacy Enhanced Mail (pem) from the public key
    This may be send to the other party

    :param public_key:  ec.EllipticCurvePublicKey
    :return: Privacy Enhanced Mail message
    :rtype: bytes
    """
    __assure_public_key(public_key)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pem


def generate_private_pem(private_key: ec.EllipticCurvePrivateKey, pwd: bytes = None) -> bytes:
    """
    Private function to make generate a pem which can be saved to store the private key
    This should never been send to the other party

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


def generate_keys(directory: str, pwd: bytes = None) -> (ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey):
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


def generate_private_key(directory: str, pwd: bytes = None) -> ec.EllipticCurvePrivateKey:
    """
    Generate the private key, this key should not be shared with anyone!
    Generated keys have a default name, you should rename them
    This can be done with os.rename()
    This should never been send to the other party

    :param directory: folder where the keys are made
                      overwrite the existing keys
    :param pwd: password: if not None, Best available encryption is chosen
    :return: ec  private key object
    """
    directory = os.path.realpath(directory)
    if not os.path.isdir(directory):
        directory = os.path.dirname(directory)

    # generate private key
    private_key = get_private_key()

    private_path = os.path.join(directory, './private_key.pem')
    with open(private_path, 'wb') as open_file:
        private_pem = generate_private_pem(private_key, pwd)
        open_file.write(private_pem)
    return private_key


def generate_public_key(directory: str, private_key: ec) -> ec.EllipticCurvePublicKey:
    """
    Generate the public key, share this key with anyone
    Generated keys have a default name, you should rename them
    This can be done with os.rename()
    This may be send to the other party

    :param directory: folder where the keys are made
                      overwrite the existing keys
    :raises InvalidKey: if given key is invalid
    :return: ec  private key object
    """
    __assure_private_key(private_key)
    public_key = private_key.public_key()
    public_path = os.path.join(directory, './public_key.pem')
    with open(public_path, 'wb') as open_file:
        public_pem = generate_public_pem(public_key)
        open_file.write(public_pem)
    return public_key


def __read_file(key_file: str) -> bytes:
    """ private function that reads a file and returns bytes """
    key_file = os.path.realpath(key_file)
    if not os.path.exists(key_file):
        raise FileNotFoundError("given file doesnt exist: {0}".format(key_file))
    with open(key_file, "rb") as key_file:
        return key_file.read()


def read_private_key(key_file: (str, bytes), pwd: bytes = None) -> ec.EllipticCurvePrivateKey:
    """
    Read and return a private key
    To use with an incoming encrypted message
    :param key_file: str  path to the keyfile
    :param pwd: bytes  if the private key is locked with an password
    :raises FileNotFoundError:  if key_file doesnt exist
    :return: serialization object
    """
    if isinstance(key_file, str) and os.path.isfile(key_file):
        key_file = __read_file(key_file)

    private_key = serialization.load_pem_private_key(key_file, password=pwd, backend=default_backend())
    return private_key


def read_public_key(key_file: str) -> ec.EllipticCurvePublicKey:
    """
    Read and return a public key
    To use with encrypting an outgoing message
    :param key_file: str
    :raises FileNotFoundError:  if key_file doesnt exist
    :return: serialization object
    """
    if isinstance(key_file, str) and os.path.isfile(key_file):
        key_file = __read_file(key_file)

    public_key = serialization.load_pem_public_key(key_file, backend=default_backend())
    return public_key


def sign_data(data: bytes, private_key: ec.EllipticCurvePrivateKey, algorithm: ec.ECDSA = None) -> bytes:
    """
    Sign data with the private key to ensure te receiving party that it is your's
    The other party needs the public key to ensure the signed data is from the expected source.
    The signature should be send with the data that is given.

    :param private_key: the private key to sign the data with
    :param data: data to sign
    :param algorithm: algorithm agreed upon with the receiving party
    :return: signature based on the data
    """
    __assure_private_key(private_key)
    if not bool(algorithm):
        algorithm = ec.ECDSA(hashes.SHA256())
    signed_data = private_key.sign(data, algorithm)
    return signed_data


# monkey patch so it is compatible with rsa.py
sign_message = sign_data


def verify_signed_data(signature: bytes, data: bytes,
                       public_key: ec.EllipticCurvePublicKey, algorithm: ec.ECDSA = None) -> bool:
    """
    Verify the received data with the public key and the signature of the source

    :param public_key: public key from the other party
    :param signature: the signature that has been send along the data
    :param data: data that belongs to the signature
    :param algorithm: algorithm used by the other party
    :return: bool
    """
    __assure_public_key(public_key)
    result = False  # set the result to False
    if not bool(algorithm) and algorithm is None:  # if algorithm is None
        algorithm = ec.ECDSA(hashes.SHA256())

    try:  # with suppress(InvalidSignature):
        public_key.verify(signature, data, algorithm)
    except InvalidSignature:
        pass  # result = False
    else:
        result = True  # no invalid signature, thus verified (True)
    finally:
        return result  # -> False if signature is invalid, True if signature is valid


# monkey patch so it is compatible with rsa.py
verify_signed_message = verify_signed_data


if __name__ == '__main__':
    print("start\n")

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("__main__").setLevel(logging.INFO)
    logging.captureWarnings(True)

    from time import time
    from tempfile import TemporaryDirectory

    original_message = b'Hello'
    print(f"original message: {original_message}")
    pwd = bytes(str(time()), 'ascii')  # pwd is the current time
    directory = TemporaryDirectory()  # create tempdir
    private_path = os.path.join(directory.name, 'private_key.pem')
    public_path = os.path.join(directory.name, 'public_key.pem')

    private_key_server = get_private_key()
    public_key_server = get_public_key(private_key_server)

    private_key_client = get_private_key()
    public_key_client = get_public_key(private_key_client)

    server_shared_key = get_shared_key(private_key_server, public_key_client)
    client_shared_key = get_shared_key(private_key_client, public_key_server)

    server_derived_key = get_derived_key(server_shared_key, b'secret')
    client_derived_key = get_derived_key(client_shared_key, b'secret')
    other_client_derived_key = get_derived_key(client_shared_key, b'another secret')

    print(server_derived_key)
    print(client_derived_key)
    print(other_client_derived_key)
    print(server_derived_key == client_derived_key)  # -> True
    print(server_derived_key == other_client_derived_key)  # -> False

    secret_data = b'secret data'
    encrypted_msg = encrypt_with_derived_key(server_derived_key, secret_data)
    uncovered_msg = decrypt_with_derived_key(client_derived_key, encrypted_msg)
    print(secret_data == uncovered_msg)  # -> True




    directory.cleanup()  # delete tempdir
