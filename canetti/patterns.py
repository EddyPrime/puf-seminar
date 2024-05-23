import numpy as np


def hamming_distance(a: list[int], b: list[int]) -> int:
    """Computes the Hamming distance between two binary vectors.

    :param a: A binary vector
    :type a: list[int]
    :param b: A binary vector
    :type b: list[int]
    :returns: the Hamming distance between a and b or -1 if a and b have different lengths
    :rtype: int
    """
    return np.count_nonzero(np.array(a) != np.array(b)) if len(a) == len(b) else -1


def complementary_hamming_distance(a: list[int], b: list[int]) -> int:
    """Computes the Hamming distance between two binary vectors.

    :param a: A binary vector
    :type a: list[int]
    :param b: A binary vector
    :type b: list[int]
    :returns: the Hamming distance between a and b or -1 if a and b have different lengths
    :rtype: int
    """
    hd = hamming_distance(a, b)
    return min(hd, len(a) - hd)


def get_pattern(size: int, lower: int = 0, upper: int = 1) -> list[int]:
    """Generates a vector of size size with values in [lower,upper].

    :param size: The number of elements in the array
    :type size: int
    :param lower: The lowerbound of each value, included (default is 0).
    :type lower: int
    :param upper: The upperbound of each value, included (default is 1).
    :type upper: int
    :returns: The array of integers
    :rtype: lst[int]
    """
    return np.random.randint(lower, upper + 1, size)


def get_pattern_from_num(size: int, num: int) -> list[int]:
    return np.array([int(x) for x in np.binary_repr(num, size)])


def get_patterns(
    size: int, N: int, lower: int = 0, upper: int = 1, num: int = None
) -> list[list[int]]:
    return (
        np.array([get_pattern_from_num(size, num) for _ in range(N)])
        if num is not None
        else np.array([get_pattern(size, lower=lower, upper=upper) for _ in range(N)])
    )


def get_pattern_float(
    size: int, lower: float = 0, upper: float = 1, decimals: int = None
) -> list[float]:
    """Generates a vector of size size with real values in [lower,upper].

    :param size: The number of elements in the array
    :type size: int
    :param lower: The lowerbound of each value, included (default is 0).
    :type lower: int
    :param upper: The upperbound of each value, included (default is 1).
    :type upper: int
    :returns: The array of integers
    :rtype: lst[int]
    """

    arr = np.random.uniform(low=lower, high=upper, size=(size,))
    return np.round(arr, decimals=decimals) if isinstance(decimals, int) else arr


def get_patterns_float(
    size: int, N: int, lower: float = 0, upper: float = 1, decimals: int = None
) -> list[list[float]]:
    return np.array(
        [
            get_pattern_float(size, lower=lower, upper=upper, decimals=decimals)
            for _ in range(N)
        ]
    )


def switch(pattern: list[int], bits: int) -> list[int]:
    res = np.array(pattern)
    to_toggle = np.random.choice(len(pattern), min(len(pattern), bits), replace=False)
    res[to_toggle] = 1 - res[to_toggle]
    return res


def print_patterns(X: list[list], verbose: bool = True):
    i = 0
    while i < len(X):
        if verbose:
            print(f"x{i} : {X[i]}")
        else:
            print(f"{X[i]}")
        i += 1
