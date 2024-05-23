"""
A module implementing digital lockers.

Canetti and Dakdouk, Eurocrypt 2008
Mihir Bellare and Phillip Rogaway. Random oracles are practical: A paradigm for designing efficient protocols. In ACM Conference on Computer and Communications Security, CCS, pages 62–73, 1993.

The lock operation is defined as
    lock(key,val) = nonce, H(nonce,key) xor (val || 0^s) = c

The unlock operation is defined as
    unlock(key',c) = H(c_0,key') xor c_2 = val'

If key' is equal to key, then val' will be equal to val.
Trailing zeroes are used to state whether c was unlocked successfully with probability 1 - 2^-s.
"""

import hashlib
import secrets


def lock(
    key: str, val: str, *, s: int = 16, alg: str = "sha-256", nbytes: int = 16
) -> tuple:
    """Digital locker lock operation.

    :param key: The key used to lock val
    :type key: str
    :param val: The value to be locked
    :type val: str
    :param s: The number of trailing zeroes to further check unlock correctness
    :type s: int
    :param alg: The hashing algorithm used to compute the result
    :type alg: str
    :param nbytes: The length in bytes of the nonce
    :type nbytes: int
    :returns: The pair < nonce, H(nonce,key) xor (val||0^s) >
    :rtype: tuple
    """

    # Generate a nonce
    nonce = secrets.token_bytes(nbytes=nbytes).hex()

    # Compute H(nonce,key)
    hash_alg = (
        hashlib.new("sha256")
        if not isinstance(alg, str) or alg not in hashlib.algorithms_guaranteed
        else hashlib.new(alg)
    )

    hash_alg.update((nonce + str(key)).encode())
    nonce_key_hash = hash_alg.hexdigest()

    # Compute (val||0^s)
    val_zero_str = str(val) + "0" * s

    # Compute H(nonce,key) xor (val||0^s)
    xor_val = int(nonce_key_hash, 16) ^ int(val_zero_str.encode().hex(), 16)

    # c = nonce , H(nonce,key) xor (val||0^s)
    c = nonce, hex(xor_val)[2:]
    return c


def unlock(key: str, c: tuple, *, s: int = 16, alg: str = "sha-256") -> str or None:  # type: ignore
    """Digital locker unlock operation.

    :param key: The key used to unlock c
    :type key: str
    :param c: The value returned by a previous lock operation
    :type c: tuple
    :param s: The number of trailing zeroes to further check unlock correctness
    :type s: int
    :param alg: The hashing algorithm used to compute the result
    :type alg: str
    :returns: The value previously locked or None if the unlocking was not correct
    :rtype: str or None
    """
    # Extract values from c, output of lock(key,val)
    try:
        nonce, xor_val = c
    except ValueError:
        print("provide the tuple returned by lock operation")
        return None

    # Compute H(nonce,key)
    hash_alg = (
        hashlib.new("sha256")
        if not isinstance(alg, str) or alg not in hashlib.algorithms_guaranteed
        else hashlib.new(alg)
    )

    hash_alg.update((nonce + str(key)).encode())
    nonce_key_hash = hash_alg.hexdigest()

    # Derive val||0^s as H(nonce,key) xor xor_val
    val_zero_str = int(nonce_key_hash, 16) ^ int(xor_val, 16)
    try:
        val = bytes.fromhex(hex(val_zero_str)[2:]).decode()
    except (UnicodeDecodeError, ValueError):
        return None

    # If s 0s are trailing, then the correct value has been unlocked
    # with probability 1 - 2^-s
    return val.rstrip("0") if "0" * s == val[-s:] else None


if __name__ == "__main__":
    key = "supersecretkey"
    val = "supersecretsecret"
    zeroes = 32
    alg = "blake2b"
    c = lock(key, val, s=zeroes, alg=alg)
    u = unlock("", "", s=zeroes, alg=alg)
    print(f"val to be locked \t\t: {val}")
    print(f"val unlocked with correct key \t: {unlock(key,c,s=zeroes,alg=alg)}")
    print(f"val unlocked with another key \t: {unlock(key[1:],c,s=zeroes,alg=alg)}")
