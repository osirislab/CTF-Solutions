primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021]
mult_div = []

from formats import *

import struct, md5

def prime_factors(n):
    i = 2
    factors = {}
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            if i in factors:
                factors[i] += 1
            else:
                factors[i] = 1
    if n > 1:
        if n in factors:
            factors[n] += 1
        else:
            factors[n] = 1

    return factors

executable = read_executable('ff2')
executable.analyze()

raw_ptrs = executable.get_binary()[0xe2e0:0xfd50]

for i in range(0, len(raw_ptrs), 8):
    p = struct.unpack('<Q', raw_ptrs[i:i+8])[0]
    mult_div.append(int(executable.strings[p].string))

_input = raw_input("String? ")

product = 1019

for i in range(0, min(len(_input), 84)):
    cur_prime = primes[i]
    cur_prime = cur_prime**ord(_input[i])
    product *= cur_prime

cont = True

while cont:
    cont = False
    for j in range(len(mult_div)/2):
        multiplicand = mult_div[2*j]
        div_by = mult_div[(2*j)+1]
        b = product * multiplicand
        if b % div_by == 0:
            product = b / div_by
            cont = True
            break


n = product
s = ''
for i in range(172):
    c = 0
    while n % primes[i] == 0:
        n = n/primes[i]
        c+=1
    if c == 0:
        break
    s += chr(c)
s+=chr(10)

l = []

for i in range(347, len(mult_div), 6):
    factors = prime_factors(mult_div[i])
    l.append(chr(factors[min(factors)]))

print 'BKPCTF{'+md5.md5(''.join(l)[:-1]+'\n').hexdigest()+'}'