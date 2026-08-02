"""Reference answers for the exercises.

Look at these only after you have tried on your own.
Names match openssl/crypto/sm4/sm4.c.
"""

MASK_32 = 0xFFFFFFFF


# Exercise 1

def rotl(a, n):
    a = a & MASK_32
    n = n % 32
    if n == 0:
        return a
    return (((a << n) & MASK_32) | (a >> (32 - n))) & MASK_32


# Exercise 2

def load_u32_be(b, n):
    i = 4 * n
    return ((b[i] << 24) | (b[i + 1] << 16) | (b[i + 2] << 8) | b[i + 3]) & MASK_32


def store_u32_be(v):
    v &= MASK_32
    return bytes([(v >> 24) & 0xFF, (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF])


# Exercise 3

def SM4_T_non_lin_sub(X):
    from sm4 import SM4_S

    X &= MASK_32
    b0 = (X >> 24) & 0xFF
    b1 = (X >> 16) & 0xFF
    b2 = (X >> 8) & 0xFF
    b3 = X & 0xFF
    return ((SM4_S[b0] << 24) | (SM4_S[b1] << 16) | (SM4_S[b2] << 8) | SM4_S[b3]) & MASK_32


# Exercise 4

def SM4_T_slow(X):
    t = SM4_T_non_lin_sub(X)
    return (t ^ rotl(t, 2) ^ rotl(t, 10) ^ rotl(t, 18) ^ rotl(t, 24)) & MASK_32


# Exercise 5

def SM4_key_sub(X):
    t = SM4_T_non_lin_sub(X)
    return (t ^ rotl(t, 13) ^ rotl(t, 23)) & MASK_32


# Exercise 6

def ossl_sm4_set_key(key):
    from sm4 import FK, CK

    if len(key) != 16:
        raise ValueError("key must be 16 bytes")
    K0 = load_u32_be(key, 0) ^ FK[0]
    K1 = load_u32_be(key, 1) ^ FK[1]
    K2 = load_u32_be(key, 2) ^ FK[2]
    K3 = load_u32_be(key, 3) ^ FK[3]
    rk = []
    for i in range(32):
        mixed = K1 ^ K2 ^ K3 ^ CK[i]
        new = (K0 ^ SM4_key_sub(mixed)) & MASK_32
        rk.append(new)
        K0, K1, K2, K3 = K1, K2, K3, new
    return rk


# Exercise 7

def ossl_sm4_encrypt(in_bytes, key):
    if len(in_bytes) != 16 or len(key) != 16:
        raise ValueError("in_bytes and key must be 16 bytes")
    rk = ossl_sm4_set_key(key)
    B0 = load_u32_be(in_bytes, 0)
    B1 = load_u32_be(in_bytes, 1)
    B2 = load_u32_be(in_bytes, 2)
    B3 = load_u32_be(in_bytes, 3)
    for i in range(32):
        mixed = (B1 ^ B2 ^ B3 ^ rk[i]) & MASK_32
        new = (B0 ^ SM4_T_slow(mixed)) & MASK_32
        B0, B1, B2, B3 = B1, B2, B3, new
    return store_u32_be(B3) + store_u32_be(B2) + store_u32_be(B1) + store_u32_be(B0)


# Exercise 8

def ossl_sm4_decrypt(in_bytes, key):
    if len(in_bytes) != 16 or len(key) != 16:
        raise ValueError("in_bytes and key must be 16 bytes")
    rk = list(reversed(ossl_sm4_set_key(key)))
    B0 = load_u32_be(in_bytes, 0)
    B1 = load_u32_be(in_bytes, 1)
    B2 = load_u32_be(in_bytes, 2)
    B3 = load_u32_be(in_bytes, 3)
    for i in range(32):
        mixed = (B1 ^ B2 ^ B3 ^ rk[i]) & MASK_32
        new = (B0 ^ SM4_T_slow(mixed)) & MASK_32
        B0, B1, B2, B3 = B1, B2, B3, new
    return store_u32_be(B3) + store_u32_be(B2) + store_u32_be(B1) + store_u32_be(B0)
