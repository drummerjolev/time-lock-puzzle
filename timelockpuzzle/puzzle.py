import functools
import os
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


def fast_exponentiation(n: int, g: int, x: int) -> int:
    # reverses binary string
    binary = bin(x)[2:][::-1]
    squares = successive_squares(g, n, len(binary))
    # keeps positive powers of two
    factors = [tup[1] for tup in zip(binary, squares) if tup[0] == '1']
    # TODO: replace with for-loop
    return functools.reduce(lambda a, b: a * b % n, factors)


def successive_squares(base: int, mod: int, length: int) -> [int]:
    table = [base % mod]
    prev = base % mod
    for n in range(1, length):
        squared = prev**2 % mod
        table.append(squared)
        prev = squared
    return table


# TODO: move to class
def encrypt(t: int, s: int):
    if not t or not s:
        # TODO: custom error handling
        raise AssertionError

    # message contains vote info
    message = b"This is a vote for John Doe"

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
    # TODO: use AES?
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
    e = fast_exponentiation(phi_n, 2, t * s)
    b = fast_exponentiation(n, a, e)

    encrypted_key = (key_int % n + b) % n
    return n, a, t, encrypted_key, encrypted_message


def decrypt(t, n):
    # TODO: use successive_squares
    # TODO: add timing?
    pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please provide t, s')
    arg_t, arg_s = sys.argv[1], sys.argv[2]
    print("t =", arg_t)
    print("s =", arg_s)
    res = encrypt(int(arg_t), int(arg_s))
    print(res)
