import os
import sys

# line required to run as script (without -m option)
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from timelockpuzzle.puzzle import encrypt


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Please time to encrypt, squarings per second, message')
    arg_t, arg_s, arg_message = sys.argv[1], sys.argv[2], sys.argv[3]

    p, q, n, a, t, encrypted_key, encrypted_message, key_int = encrypt(
        arg_message.encode(),
        int(arg_t),
        int(arg_s)
    )
    print(p, q, n, a, t, encrypted_key, encrypted_message.decode(), key_int)
    sys.stdout.flush()

