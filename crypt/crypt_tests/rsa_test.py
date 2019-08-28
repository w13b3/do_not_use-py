#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rsa_test.py

import random
import string
import unittest
from crypt.rsa import *


class RsaTest(unittest.TestCase):

    @staticmethod
    def generate_pwd() -> str:
        """ Generates a random string of numbers, lower- and uppercase chars. """
        rand_str = ''
        all_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for i in range(random.randint(1, 100)):
            rand_str = ''.join(random.choice(all_chars))
        return rand_str

    @classmethod
    def setUpClass(cls) -> None:
        cls.bob_dir = TemporaryDirectory(prefix='bob')
        cls.alice_dir = TemporaryDirectory(prefix='alice')
        cls.bobs_pwd = bytes(cls.generate_pwd(), 'ascii')
        cls.alices_pwd = bytes(cls.generate_pwd(), 'ascii')
        cls.bobs_private_key, cls.bobs_public_key = generate_keys(cls.bob_dir.name, cls.bobs_pwd)
        cls.alices_private_key, cls.alices_public_key = generate_keys(cls.alice_dir.name, cls.alices_pwd)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.bob_dir.cleanup()
        cls.alice_dir.cleanup()

    def test_keys_saved_are_equal_to_generated(self):
        """
        saved private key can make public keys that are the same as the saved public keys
        this verifies the uniqueness of the public key
        also that more public keys can derive from the private key
        """
        # bobs keys
        bob_private_path = os.path.join(self.bob_dir.name, 'private_key.pem')
        bob_public_path = os.path.join(self.bob_dir.name, 'public_key.pem')
        read_bob_private_key = read_private_key(bob_private_path, self.bobs_pwd)
        read_bob_public_key = read_public_key(bob_public_path)

        local_bob_public_key = read_bob_private_key.public_key()
        self_bob_public_key = self.bobs_private_key.public_key()
        bobs_public_nr1 = local_bob_public_key.public_numbers()
        bobs_public_nr2 = self_bob_public_key.public_numbers()
        bobs_public_nr3 = read_bob_public_key.public_numbers()
        bobs_public_nr4 = self.bobs_public_key.public_numbers()
        self.assertTrue(
            bobs_public_nr1 == bobs_public_nr2 == bobs_public_nr3 == bobs_public_nr4
        )
        # alices keys
        alice_private_path = os.path.join(self.alice_dir.name, 'private_key.pem')
        alice_public_path = os.path.join(self.alice_dir.name, 'public_key.pem')
        read_alice_private_key = read_private_key(alice_private_path, self.alices_pwd)
        read_alice_public_key = read_public_key(alice_public_path)

        local_alice_public_key = read_alice_private_key.public_key()
        self_alice_public_key = self.alices_private_key.public_key()
        alices_public_nr1 = local_alice_public_key.public_numbers()
        alices_public_nr2 = self_alice_public_key.public_numbers()
        alices_public_nr3 = read_alice_public_key.public_numbers()
        alices_public_nr4 = self.alices_public_key.public_numbers()
        self.assertTrue(
            alices_public_nr1 == alices_public_nr2 == alices_public_nr3 == alices_public_nr4
        )

        self.assertFalse(bobs_public_nr1 == alices_public_nr1)
        self.assertFalse(bobs_public_nr2 == alices_public_nr2)
        self.assertFalse(bobs_public_nr3 == alices_public_nr3)
        self.assertFalse(bobs_public_nr4 == alices_public_nr4)

    def test_signed_message_can_be_verified(self):
        """
        bob sends a message to alice, he signs the message with his private key
        alice has the public key from bob.
        when alice receives the message from bob, she checks the authenticity by using bob's public key
        """
        # alice sends a message to bob and signs it with her private key
        message_to_bob = b'hello bob'
        signed_by_alice = sign_message(message_to_bob, self.alices_private_key)
        # bob receives the message and to make sure it comes from alice, bob uses alice's public key to verify it
        verified_from_alice = verify_signed_message(signed_by_alice, message_to_bob, self.alices_public_key)
        self.assertTrue(verified_from_alice)

        # bob sends a message to alice and signs it with his private key
        message_to_alice = b'hello alice'
        signed_by_bob = sign_message(message_to_alice, self.bobs_private_key)
        # alice receives the message and to make sure it comes from bob, alice uses bob's public key to verify it
        verified_from_bob = verify_signed_message(signed_by_bob, message_to_alice, self.bobs_public_key)
        self.assertTrue(verified_from_bob)

        # john doesnt like bob so he intercepts the message from alice and alters it
        message_to_alice = b'goodbye alice'
        # alice receives the message and assumes it comes from bob, to be sure she verifies it with bob hos public key
        verified_from_bob = verify_signed_message(signed_by_bob, message_to_alice, self.bobs_public_key)
        self.assertFalse(verified_from_bob)  # alice now knows bob didn't send this message

    def test_encryption_decryption(self):
        """
        alice has the public key from bob
        alice wants to send a secret message to bob
        alice encrypts the message with the public key from bob
        bob receives the encrypted message from alice
        bob uses his private key to decrypt the message
        now bob can read the message send by alice
        """
        # bob sends an encrypted message with alice's public key to alice
        message_to_alice = b'hello alice'
        encrypted_by_bob = rsa_encrypt(message_to_alice, self.alices_public_key)
        # alice receives the message and decrypt the message with her private key
        decrypted_by_alice = rsa_decrypt(encrypted_by_bob, self.alices_private_key)
        self.assertEqual(message_to_alice, decrypted_by_alice)

        # alice sends an encrypted message with bob's public key to bob
        message_to_bob = b'hello bob'
        encrypted_by_alice = rsa_encrypt(message_to_bob, self.bobs_public_key)
        # bob receives the message and decrypt the message with his private key
        decrypted_by_bob = rsa_decrypt(encrypted_by_alice, self.bobs_private_key)
        self.assertEqual(message_to_bob, decrypted_by_bob)

        # john doesnt like bob so he intercepts the message from alice and sends his own
        message_to_bob = b'goodbye bob'
        encrypted_by_john = rsa_encrypt(message_to_bob, self.bobs_public_key)
        # bob receives the message and decrypt the message with his private key
        decrypted_by_bob = rsa_decrypt(encrypted_by_john, self.bobs_private_key)
        self.assertEqual(message_to_bob, decrypted_by_bob)  # bob now thinks alice says goodbye


if __name__ == '__main__':
    unittest.main()