import os
import sys

from timelockpuzzle.algorithms.fast_exponentiation import fast_exponentiation

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


# TODO: move to class
def encrypt(message: bytes, seconds: int, squarings_per_second: int):
    if not seconds or not squarings_per_second:
        raise AssertionError

    # hard code safe exponent to use
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # see RSA for security specifications
    p, q = private_key.private_numbers().p, private_key.private_numbers().q
    n = private_key.public_key().public_numbers().n
    phi_n = (p - 1) * (q - 1)

    # Fernet is an asymmetric encryption protocol using AES
    key = Fernet.generate_key()
    key_int = int.from_bytes(key, sys.byteorder)
    cipher_suite = Fernet(key)

    # Vote Encryption
    encrypted_message = cipher_suite.encrypt(message)

    # Pick safe, pseudo-random a where 1 < a < n
    # Alternatively, we could use a = 2
    a = int.from_bytes(os.urandom(32), sys.byteorder) % n + 1

    # Key Encryption
    t = seconds * squarings_per_second
    e = 2**t % phi_n
    b = fast_exponentiation(n, a, e)

    encrypted_key = (key_int % n + b) % n
    return n, a, t, encrypted_key, encrypted_message, key_int


def decrypt(n: int, a: int, t: int, enc_key: int, enc_message: int):
    # Successive squaring to find b
    # We assume this cannot be parallelized
    b = a % n
    for i in range(t):
        b = b**2 % n
    dec_key = (enc_key - b) % n

    # Retrieve key, decrypt message
    key_bytes = int.to_bytes(dec_key, length=64, byteorder=sys.byteorder)
    cipher_suite = Fernet(key_bytes)
    return cipher_suite.decrypt(enc_message)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please provide t, s')
    arg_t, arg_s = sys.argv[1], sys.argv[2]
    print("t =", arg_t)
    print("s =", arg_s)
    n, a, t, encrypted_key, encrypted_message, original_key = encrypt(b"This is a vote for Myrto", int(arg_t), int(arg_s))
    print('Decrypting')
    dec_msg = decrypt(n, a, t, encrypted_key, encrypted_message)
    print(dec_msg)
