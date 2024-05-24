"""
A module implementing Canetti et al. fuzzy extractor.

Ran Canetti et al. “Reusable fuzzy extractors for low-entropy distributions”.
In: Journal of Cryptology 34 (2021), pp. 1–33.

The lock operation is defined as
    lock(key,val) = nonce, H(nonce,key) xor (val || 0^s) = c

The unlock operation is defined as
    unlock(key',c) = H(c_0,key') xor c_2 = val'

If key' is equal to key, then val' will be equal to val.
Trailing zeroes are used to state whether c was unlocked successfully with probability 1 - 2^-s.
"""

import math
import secrets

import numpy as np

import digitallocker as dl


def set_l(n: int, k: int, t: float, delta: float) -> int:
    """Compute parameter l.

    :param n: Length of the reading.
    :type n: int
    :param k: Lenght of the key.
    :type k: int
    :param t: Error tolerance.
    :type t: float
    :param delta: Fuzzy extractor error rate.
    :type delta: float
    :returns: The number of helper data entries.
    :rtype: int
    """
    return (
        0
        if n < 2 or k < 1 or t < 1 or delta < 0 or delta > 1
        else int(n ** math.ceil((t * k) / (n * math.log(n))) * math.log2(4 / delta))
    )


def gen(w: list[int], k: int, t: float, delta: float = 0.5) -> tuple:
    """Canetti et al. fuzzy extractor generate preocedure.

    :param w: Reference reading.
    :type w: list[int]
    :param k: Lenght of the key.
    :type k: int
    :param t: Error tolerance.
    :type t: float
    :param delta: Fuzzy extractor error rate.
    :type delta: float
    :returns: The tuple constituted by the key and the helper data.
    :rtype: tuple
    """
    # 1. Input w = w_1, ... , w_n
    n = np.shape(w)[0]

    # 2. Sample r <--$-- {0,1}^k
    r = str(secrets.token_bytes(k // 8))

    # 3. For i = 1,...,l
    l = set_l(n, k, t, delta)
    p = [0 for _ in range(0, l)]
    for i in range(0, l):
        # 3.i   Choose random 1 <= j_i,1 , ... , j_i,k <= n
        ji = np.random.randint(low=0, high=n, size=k)

        # 3.ii  Set v_i = w_j_i,1 , ... , w_j_i,k
        # vi = [w[ji[i], i] for i in range(0, k)]
        vi = [w[ji[j]] for j in range(0, k)]

        # 3.iii Set c_i = lock(v_i , r)
        ci = dl.lock(vi, r)

        # 3.iv  Set p_i = c_i , (j_i,1 , ... , j_i,k)
        p[i] = ci, ji

    # 4. Output (r,p), where p = (p_1, ... , p_l)
    return r, p


def rep(wprime: list[int], p: tuple) -> str or None:  # type: ignore
    """Canetti et al. fuzzy extractor reproduce preocedure.

    :param wprime: Possibly noisy reading.
    :type wprime: list[int]
    :param p: Helper data producec by a previous generation procedure.
    :type p: tuple
    :returns: The key if reproduction is successful or nothing.
    :rtype: str or None
    """
    # 1. Input w' = w'_1, ... , w'_n , p = p_1, ... , p_l
    n = np.shape(wprime)[0]

    # 2. For i = 1,...,l
    for i in range(0, len(p)):
        # 2.i   Parse p_i = c_i , (j_i,1 , ... , j_i,k)
        try:
            ci, ji = p[i]
        except ValueError:
            print("provide the tuple returned by gen")
            return None

        # 2.ii  Set v_i = w'_j_i,1 , ... , w'_j_i,k
        # vi = [wprime[ji[i], i] for i in range(0, k)]
        vi = [wprime[ji[j]] for j in range(0, k)]

        # 2.iii Set r_i = unlock(v'_i,c_i).
        #       If r_i != None output r_i
        ri = dl.unlock(vi, ci)
        if ri:
            return ri

    # 3. Output None
    return None


def get_size_of_helper_data_bits(n, helper_data):
    (nonce, hash), j = helper_data[0]
    # print(f"|nonce| = {len(nonce)}")
    # print(f"|hash| = {len(hash)}")
    return len(helper_data) * (
        len(nonce) * 4 + len(hash) * 4 + len(j) * math.ceil(math.log2(n))
    )


if __name__ == "__main__":
    from patterns import get_pattern, switch
    import time
    from tqdm import tqdm
    from random import randrange

    with open("../arduino/data.txt") as f:
        lines = [[int(x) for x in line.strip()] for line in f.readlines()]

    random_w = 1

    n = 1024 if random_w else len(lines[0])  # length of puf response
    k = 80  # length of key
    eabs = 0.03  # absolute error rate of puf
    t = math.ceil(n * eabs)  # number of bits to tolerate
    delta = 0.0018 * 2  # error rate of rep
    l = set_l(n, k, t, delta)  # canetti parameter

    print(f"n       : {n}")
    print(f"k       : {k}")
    print(f"eabs    : {eabs}")
    print(f"t       : {t}")
    print(f"delta   : {delta}")
    print(f"l       : {l}")

    experiments = 10  # number of experiments
    execution_time = 0
    errors = 0
    helper_data_size = 0

    print(
        f"{'randomly generating strings' if random_w else 'retrieving strings from readings'}"
    )

    for i in tqdm(range(0, experiments)):
        w = (
            np.array(get_pattern(n))
            if random_w
            else np.array(lines[randrange(len(lines))])
        )

        start_time = time.time()
        key, helper_data = gen(w, k, t, delta)
        gen_time = time.time() - start_time

        wprime = (
            np.array(switch(w, t))
            if random_w
            else np.array(lines[randrange(len(lines))])
        )

        start_time = time.time()
        key_rep = rep(wprime, helper_data)
        rep_time = time.time() - start_time

        # print(f"key\t\t{key}")
        # print(f"key_rep\t\t{key_rep}")
        # print(f"correctly reproduced? {'yes' if key_rep == key else 'no'}")

        errors += 0 if key_rep == key else 1

        # print(f"gen_time : {gen_time}")
        # print(f"rep_time : {rep_time}")
        # print(f"tot_time : {gen_time + rep_time}")

        execution_time += gen_time + rep_time

        helper_data_size += get_size_of_helper_data_bits(n, helper_data) // 8

    print(f"errors        : {errors}")
    print(f"time      (s) : {round(execution_time / experiments,9)}")
    print(f"memory (bits) : {round(helper_data_size / experiments,3)}")
