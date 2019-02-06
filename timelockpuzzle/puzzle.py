import os
import sys
import time

from timelockpuzzle.algorithms.fast_exponentiation import fast_exponentiation

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


# TODO: move to class
def encrypt(seconds: int, squarings_per_second: int):
    # TODO: find safe seconds to use
    if not seconds or not squarings_per_second:
        # TODO: custom error handling
        raise AssertionError

    # message contains vote info
    message = b"This is a vote for Myrto"

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # used to compute phi_n
    p, q = private_key.private_numbers().p, private_key.private_numbers().q

    # save for later
    n = private_key.public_key().public_numbers().n

    # encrypt vote
    # Fernet is an asymmetric encryption protocol using AES
    # TODO: this key is probably unsafe.
    # TODO: Fernet uses AES under the hood. Maybe use directly?
    key = Fernet.generate_key()
    key_int = int.from_bytes(key, sys.byteorder)

    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message)

    # pick random a
    # TODO: to helper. Choose fixed 2, as mentioned in the paper?
    a = int.from_bytes(os.urandom(32), sys.byteorder) % n + 1

    # Encrypt key
    # Hardness assumption: factoring phi_n
    phi_n = (p - 1) * (q - 1)
    t = seconds * squarings_per_second
    e = 2**t % phi_n
    b = fast_exponentiation(n, a, e)

    encrypted_key = (key_int % n + b) % n
    return n, a, t, encrypted_key, encrypted_message, key_int


def decrypt(n: int, a: int, t: int, enc_key: int, enc_message: int):
    before = time.time()
    b = a % n
    for i in range(t):
        b = b**2 % n
    print('It took:', time.time() - before)
    dec_key = (enc_key - b) % n

    key_bytes = int.to_bytes(dec_key, length=64, byteorder=sys.byteorder)
    cipher_suite = Fernet(key_bytes)
    return cipher_suite.decrypt(enc_message)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please provide t, s')
    arg_t, arg_s = sys.argv[1], sys.argv[2]
    print("t =", arg_t)
    print("s =", arg_s)
    # TODO: function for time counting
    n, a, t, encrypted_key, encrypted_message, original_key = encrypt(int(arg_t), int(arg_s))
    print('Decrypting')
    # decrypt
    dec_msg = decrypt(n, a, t, encrypted_key, encrypted_message)
    print(dec_msg)
