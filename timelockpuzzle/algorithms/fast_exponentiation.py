def fast_exponentiation(n: int, g: int, x: int) -> int:
    # reverses binary string
    binary = bin(x)[2:][::-1]
    squares = successive_squares(g, n, len(binary))
    # keeps positive powers of two
    factors = [tup[1] for tup in zip(binary, squares) if tup[0] == '1']
    acc = 1
    for factor in factors:
        acc = acc * factor % n
    return acc


def successive_squares(base: int, mod: int, length: int) -> [int]:
    table = [base % mod]
    prev = base % mod
    for n in range(1, length):
        squared = prev**2 % mod
        table.append(squared)
        prev = squared
    return table
