import binascii, sys, struct

x = sys.argv[1].decode('hex')
delta = '\x00'*10 + '\x01' + '\x00'*17
delta += struct.pack('<L', 0xef52b6e1)
print(''.join(chr(ord(a)^ord(d)) for a,d in zip(x, delta)).encode('hex'))