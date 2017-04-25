from pwn import *
import random

r = remote('bb8.chal.pwning.xxx', 20811)

vals = []
correct_idxs = []

for i in range(600):
    r.sendline('y') # a->b key dist; yes intercept
    basis = ['Y', 'Z'][random.randint(0,1)]
    r.sendline(basis) # basis
    vals.append([basis, None])
    r.sendline('n') # forward existing
    if i == 599:
        break
    r.sendline('y') # b->a, ACKing the bit
    r.sendline('Z')
    r.sendline('n')

for i in range(600):
    r.recvuntil('to Bob, do you want to intercept (y/N)?')
    r.recvuntil('measured ')
    val = int(r.recvuntil('\n'))
    vals[i][1] = val
    if i == 599:
        break
    r.recvuntil('to Alice, do you want to intercept (y/N)?')
    r.recvuntil('measured ')
    assert int(r.recvuntil('\n')) == 1


print "Got vals", vals

# Bits now received, intercept all b->a confirmations and replace with our own; also intercept a->b 
for i in range(600):
    #r.recvuntil('?\n')
    r.sendline('y') # b->a, sending measured basis; replace with ours
    #r.recvline()
    r.sendline('Z')
    #r.recvuntil('?\n') # replace?
    r.sendline('y')
    #r.recvline()
    r.sendline('Z')
    #r.recvline()
    r.sendline('-1' if vals[i][0] == 'Z' else '1')
    
    #r.recvuntil('?\n')
    r.sendline('y') # a->b correctness
    #r.recvline()
    r.sendline('Z') # correctness is always in the Z basis
    
    r.sendline('n') # forward existing

for i in range(600):
    r.recvuntil('to Alice, do you want to intercept (y/N)?')
    r.recvuntil('to Bob, do you want to intercept (y/N)?')
    r.recvuntil('measured ')
    val = int(r.recvuntil('\n'))
    if val == 1:
        correct_idxs.append(i)

print "Got correct idxs", correct_idxs
print "len(correct) =", len(correct_idxs)

#r.interactive()

# B takes every other measurement he made and send it to Alice to verify. 
for i in correct_idxs[::2]:
    r.sendline('y') # b->a, sending measured values; replace with ours
    r.sendline('Z')
    r.sendline('y')
    r.sendline('Z')
    r.sendline(str(vals[i][1]))
    
    r.sendline('y') # a->b ACK
    r.sendline('Z')
    r.sendline('n')

for i in correct_idxs[::2]:
    print i, r.recvuntil('to Alice, do you want to intercept (y/N)?')
    print i, r.recvuntil('to Bob, do you want to intercept (y/N)?')
    print i, r.recvuntil('measured ')
    assert int(r.recvuntil('\n')) == 1

aes_k = 0
for i in correct_idxs[1::2][:128]:
    aes_k <<= 1
    aes_k |= 0 if vals[i][1] == -1 else 1

# classical message
from Crypto import Random
from Crypto.Cipher import AES

r.recvuntil(')\n')
r.sendline('n')
r.recvuntil('classical message (')
msg = r.recvuntil(')')[:-1]
aes = AES.new(hex(aes_k)[2:].decode('hex'), AES.MODE_ECB, Random.new().read(32))
print aes.decrypt(msg.decode('hex'))