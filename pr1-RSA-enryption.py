import Crypto
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class Client:
    def __init__(self):
        # Creating a random number generator for key generation
        random_generator = Crypto.Random.new().read

        # Creating new public key and private key with 1024-bit modulus
        self._private_key = RSA.generate(1024, random_generator)
        self._public_key = self._private_key.publickey()

        # Initializing signer for digital signatures
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        # Returns the public key in a hexadecimal string format
        return binascii.hexlify(
            self._public_key.exportKey(format='DER')
        ).decode('ascii')

    def encrypt_message(self, public_key_hex, message):
        """
        Encrypts a message using the recipient's public key.
        """
        try:
            recipient_public_key = RSA.import_key(
                binascii.unhexlify(public_key_hex)
            )
            cipher_rsa = PKCS1_OAEP.new(recipient_public_key)
            encrypted_msg = cipher_rsa.encrypt(message.encode('utf-8'))
            return encrypted_msg
        except ValueError as e:
            print(f"Error encrypting message: {e}")
            return None

    def decrypt_message(self, encrypted_message):
        """
        Decrypts an encrypted message using the client's private key.
        """
        try:
            cipher_rsa = PKCS1_OAEP.new(self._private_key)
            decrypted_msg = cipher_rsa.decrypt(encrypted_message).decode('utf-8')
            return decrypted_msg
        except ValueError as e:
            print(f"Error decrypting message: {e}")
            return None

    def sign_message(self, message):
        """
        Signs a message using the client's private key.
        """
        h = SHA.new(message.encode('utf-8'))
        signature = self._signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    def verify_signature(self, public_key_hex, message, signature_hex):
        """
        Verifies a message's signature using the sender's public key.
        """
        try:
            sender_public_key = RSA.import_key(
                binascii.unhexlify(public_key_hex)
            )
            verifier = PKCS1_v1_5.new(sender_public_key)
            h = SHA.new(message.encode('utf-8'))
            return verifier.verify(h, binascii.unhexlify(signature_hex))
        except (ValueError, TypeError) as e:
            print(f"Error verifying signature: {e}")
            return False


# ---------------- DEMO ----------------
print("-" * 50)
print("Practical 1a: Secure Messaging Application")
print("-" * 50)

# Create two clients
alice = Client()
bob = Client()

print("Alice's Public Key (Identity):", alice.identity)
print("Bob's Public Key (Identity):", bob.identity)

print("-" * 50)

# Alice sends message to Bob
original_message_alice_to_bob = "Hello Bob, this is a secret message from Alice!"
print(f"Alice's original message: {original_message_alice_to_bob}")

encrypted_message_from_alice = alice.encrypt_message(
    bob.identity,
    original_message_alice_to_bob
)

if encrypted_message_from_alice:
    print(f"Encrypted message: {encrypted_message_from_alice}")
    print("-" * 50)

    decrypted_message_by_bob = bob.decrypt_message(encrypted_message_from_alice)

    if decrypted_message_by_bob:
        print(f"Bob decrypted message: {decrypted_message_by_bob}")
        print("Decryption successful:",
              original_message_alice_to_bob == decrypted_message_by_bob)
    else:
        print("Bob failed to decrypt the message.")
else:
    print("Encryption failed.")

print("-" * 50)

# Bob sends signed message
original_message_bob_to_alice = "Alice, I received your message. Thanks!"
print(f"Bob's original message: {original_message_bob_to_alice}")

signature_by_bob = bob.sign_message(original_message_bob_to_alice)
print(f"Bob's signature: {signature_by_bob}")

print("-" * 50)

# Alice verifies signature
is_signature_valid = alice.verify_signature(
    bob.identity,
    original_message_bob_to_alice,
    signature_by_bob
)
print(f"Alice verifies Bob's signature: {is_signature_valid}")

# Tampered message test
tampered_message = "Alice, I received your message. Thanks! (but I changed it)"

is_tampered_signature_valid = alice.verify_signature(
    bob.identity,
    tampered_message,
    signature_by_bob
)

print("Tampered verification:",
      is_tampered_signature_valid, "(should be False)")

print("-" * 50)
