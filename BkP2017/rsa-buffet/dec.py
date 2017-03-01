import gmpy, sys
import ContinuedFractions, Arithmetic

from Crypto.PublicKey import RSA
from encrypt import decrypt
from fermat_crack import *

keys = [None]*10
plaintexts = [None]*5

def try_decrypt(k):
    for c in range(5):
        x = decrypt(k, open('ciphertext-{}.bin'.format(c+1)).read())
        if x is not None:
            plaintexts[c] = x
            print "Got plaintext:", x

def load_key(n):
    return RSA.importKey(open('key-{}.pem'.format(n)).read())

print "Stage 1 - GCD"
for i in range(10):
    k1 = load_key(i)
    for j in range(i+1, 10):
        k2 = load_key(j)
        g = gmpy.gcd(k1.n, k2.n)
        if g != 1:
            p = long(g)
            q = long(k1.n / p)
            phi = (p-1) * (q-1)
            keys[i] = RSA.construct((k1.n, k1.e, long(gmpy.invert(k1.e, phi)), p, q))
            try_decrypt(keys[i])

            q = long(k2.n / p)
            phi = (p-1) * (q-1)
            keys[j] = RSA.construct((k2.n, k2.e, long(gmpy.invert(k2.e, phi)), p, q))
            try_decrypt(keys[j])

print "Stage 2 - Wiener"
sys.setrecursionlimit(2000)

def wiener(e, n):
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)

    for (k,d) in convergents:
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s*s - 4*n
            if(discr>=0):
                t = Arithmetic.is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    return d

for i in range(10):
    if keys[i] is None:
        k = load_key(i)
        x = wiener(k.e, k.n)
        if x is not None:
            impl = RSA.RSAImplementation(use_fast_math=False)
            partial = impl.construct((k.n, 0L))
            partial.key.e = k.e
            partial.key.d = x
            keys[i] = partial
            try_decrypt(keys[i])

# Found with factorization outside the script
plaintexts[0] = """Congratulations, you decrypted a ciphertext!  One down, two to go :)
1-32a1cd9f414f14cff6685879444acbe41e5dba6574a072cace6e8d0eb338ad64910897369b7589e6a408c861c8e708f60fbbbe91953d4a73bcf1df11e1ecaa2885bed1e5a772bfed42d776a9
1-e0c113fa1ebea9318dd413bf28308707fd660a5d1417fbc7da72416c8baaa5bf628f11c660dcee518134353e6ff8d37c
1-1b8b6c4e3145a96b1b0031f63521c8df58713c4d6d737039b0f1c0750e16e1579340cfc5dadef4e96d6b95ecf89f52b8136ae657c9c32e96bf4384e18bd8190546ff5102cd006be5e1580053
1-c332b8b93a914532a2dab045ea52b86d4d3950a990b5fc5e041dce9be1fd3912f9978cad009320e18f4383ca71d9d79114c9816b5f950305a6dd19c9f458695d52"""

from secretsharing import PlaintextToHexSecretSharer as SS

print SS.recover_secret(x.split('\n')[2] for x in plaintexts if x is not None)
