# Useful: https://www.fireeye.com/blog/threat-research/2015/04/analysis_of_kriptovo.html

import struct

def read_num(stream):
    length = struct.unpack('<I', stream.read(4))[0]
    raw = stream.read(length)[::-1]
    return int(raw.encode('hex'), 16)

def parse_lb_chunk(stream):
    assert stream.read(10) == 'N\nLockBox3'
    version = struct.unpack('<I', stream.read(4))[0]
    things = struct.unpack('<B', stream.read(1))[0]
    if things == 0xd:
        n = read_num(stream)
        d = read_num(stream)
        p = read_num(stream)
        q = read_num(stream)
        dp = read_num(stream)
        dq = read_num(stream)
        qinv = read_num(stream)
        
        return {'n': n, 'd': d, 'p': p, 'q': q, 'dp': dp, 'dq': dq, 'qinv': qinv}
    else:
        print 'idk what 2 do'

att = open('pcap_extracted/attachment')
first = parse_lb_chunk(att)
second = parse_lb_chunk(att)

from Crypto.PublicKey import RSA

# Why are there two keys?

first = RSA.construct((first['n'], 65537L, first['d'])) # Assuming the default 65537 is used...
second = RSA.construct((second['n'], 65537L, second['d']))





"""
ASSUMPTIONS:
* The 0x20000000 is a little endian int representing the number of bytes that the AES key take up.
* The IV is set by the first 8 bytes as mentioned in the SO questions
* CBC is used

Right now I'm mostly confused as to how the data is ever supposed to align.
There seemingly has to be 6 or so bytes used somewhere to make the ciphertext a nice multiple of 16
"""

enc = open('flag.docx.just')

key_iv_enc = enc.read(struct.unpack('<I', enc.read(4))[0])
ciphertext = enc.read()

key_iv = first.decrypt(key_iv_enc)

# https://stackoverflow.com/questions/26765881/turbopower-lockbox-3-remove-salt
# https://stackoverflow.com/questions/12138244/aes-encrypt-decrypt-delphi-php/12138580#12138580

# The first 8 bytes (64 bits) is the salt nonce. It is also the low 64 bits of the IV. The high 64 bits of the IV are zero.
iv = '\x00' * 8 + enc.read(8)

from Crypto.Cipher import AES

cipher = AES.new(aes_k, AES.MODE_CBC, iv) # Assuming CBC

plain = cipher.decrypt(ciphertext)

assert plain.startswith('PK')

print 'yay!'