import sys

bits = [0b1, 0b11, 0b1, 0b111, 0b1, 0b11, 0b1, 0b1111]
bits += [0b1, 0b11, 0b1, 0b111, 0b1, 0b11, 0b1, 0b11111]
bits += [0b1, 0b11, 0b1, 0b111, 0b1, 0b11, 0b1, 0b1111]
bits += [0b1, 0b11, 0b1, 0b111, 0b1, 0b11, 0b1, 0b111111]
bits += [0b1, 0b11, 0b1, 0b111, 0b1, 0b11, 0b1, 0b1111]
bits += [0b1, 0b11, 0b1, 0b111, 0b1]

def cipher(s):
    res = [0]*len(s)
    
    res[0] = s[0]
    for i in range(len(s)):
    	res[0] = res[0] ^ bits[i]
    
    for c in range(1,len(s)):
    	res[c] = res[c-1] ^ s[c]
    
    return res

s="60 00 0c 3a 1e 52 02 53 02 51 0c 5d 56 51 5a 5f 5f 5a 51 00 05 53 56 0a 5e 00 52 05 03 51 50 55 03 04 52 04 0f 0f 54 52 57 03 52 04 4e".split(' ')
s=[int(x,16) for x in s]
print ''.join([chr(x) for x in cipher(s)])