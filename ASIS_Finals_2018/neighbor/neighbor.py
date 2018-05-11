#!/usr/bin/env python
from pwn import *
import hashlib
import itertools
import numpy as np

context.log_level = "debug"
p = remote("37.139.22.174", 11740)
p.recvuntil("Submit")
ln = p.recvn(len("a printable string X, such that sha256(X)[-6:] = 10d36290"))
brute_str = ln.split(" = ")[-1].strip()
print(brute_str)

def brute():
    for count in range(1,126):
        for i in itertools.combinations(range(32, 126), count):
            string = "".join(map(chr,i))
            sha = hashlib.sha256(bytes(string))
            if sha.hexdigest()[-6:] == brute_str:
                print(string)
                return string

p.sendline(brute())
p.recvline()
p.recvline()

n = int(p.recvline().split(" = ")[-1].strip())
#p.interactive()

def pcomp(n):
    p2 = 1;
    i = 0;
    while( p2 < n ):
        p2 = np.left_shift(p2, 2);
        i = np.add(i, 2);
    
    p2= np.right_shift(p2, 2);
    i = np.subtract(i, 2);
    p2  = np.right_shift(p2, i/2)
    return p2


def squareLowerThan(n):
    p = pcomp(n)
    p2 = np.square(p)
    d = 1; 
    while( p2 + np.multiply(2,p) + d < n ):
        p2 = np.add(p2, np.multiply(2,p) + d);
        d = np.add(d, 2);
    return p2;

ans = squareLowerThan(n)
print(ans)
p.sendline(str(ans))
print p.recvall()
