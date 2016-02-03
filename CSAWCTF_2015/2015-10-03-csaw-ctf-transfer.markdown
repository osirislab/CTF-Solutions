---
author: ghost
comments: true
date: 2015-10-03 11:37+00:00
layout: post
slug: csaw-ctf-transfer
title: CSAW CTF 2015 - Transfer
---

After quickly looking through the .pcap, we find two things: a python source file, and a large b64 string ('2Mk16Sk5iakYx...')

```python
import string
import random
from base64 import b64encode, b64decode

enc_ciphers = ['rot13', 'b64e', 'caesar']
dec_ciphers = ['rot13', 'b64decode', 'caesard']

def rot13(s):
    _rot13 = string.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    return string.translate(s, _rot13)

def b64e(s):
    return b64encode(s)

def caesar(plaintext, shift=3):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)

def caesard(s, shift=3):
    return caesar(s, shift=-shift)

def encode(pt, cnt=50):
    tmp = '2{}'.format(b64encode(pt))
    for cnt in xrange(cnt):
        c = random.choice(enc_ciphers)
        i = enc_ciphers.index(c) + 1
        _tmp = globals()[c](tmp)
        tmp = '{}{}'.format(i, _tmp)

    return tmp
```

After extracting both, we looked over the code extracted and see that the string is some encoded with some combination of rot13, base64, and a caesar cipher with shift=3. We see that the first character of the string at any point in decrypting is going to be the cipher by which the following text is encoded, so the problem is incredibly simple. We define

    dec_ciphers = [‘rot13’, ‘b64decode’, ‘caesard’]

and

    caesard(s, shift=3) as caesar(s, shift=-shift)

at the end of the extracted python file, and finally create the extraction loop:

```python
t = b64decode(s[1:]) # s is the provided encoded string

while True:
    choice = int(t[0]) - 1
    s = t[1:]
    t = globals()[dec_ciphers[choice]](s)
    print t
```

This code simply errors out when the flag is hit. Crude but effective.
