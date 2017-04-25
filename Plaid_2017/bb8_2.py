# bb8.py reliably get's the A->B message.
# this code is really bad but worked just well enough to get the B->A message

from pwn import *
import random

#r = remote('bb8.chal.pwning.xxx', 20811)
r = remote('54.174.124.206', 20811)

a2e_vals = []
a2e_correct_idxs = []

e2b_vals = []
e2b_correct_idxs = []

for i in range(600):
    e2b_vals.append(['Z', -1])

for i in range(600):
    r.sendline('y') # a->b qubit dist; do intercept
    basis = random.choice(['Y', 'Z'])
    r.sendline(basis) # basis
    a2e_vals.append([basis, None])
    
    r.sendline('y') # modify for e->b
    r.sendline(e2b_vals[i][0])
    r.sendline(str(e2b_vals[i][1]))
    if i == 599:
        break
    
    r.sendline('y') # b->a, ACKing the bit
    r.sendline('Z')
    r.sendline('n')

for i in range(600):
    r.recvuntil('to Bob, do you want to intercept (y/N)?')
    r.recvuntil('measured ')
    val = int(r.recvuntil('\n'))
    a2e_vals[i][1] = val
    if i == 599:
        break
    
    r.recvuntil('to Alice, do you want to intercept (y/N)?')
    r.recvuntil('measured ')
    assert int(r.recvuntil('\n')) == 1 # assert B ACK

print "Got a2e vals", a2e_vals
print "Got e2b vals", e2b_vals


context.log_level = "DEBUG"

# Bits now received, intercept all b->a confirmations and replace with our own; also intercept a->b 
for i in range(600):
    print i
    r.recvuntil('to Alice, do you want to intercept (y/N)?')
    r.sendline('y') # b->a, sending measured basis; replace with ours
    r.sendline('Z')
    r.recvuntil('measured ')
    b_guessed_basis = 'Z' if int(r.recvuntil('\n')) == -1 else 'Y'
    r.sendline('y')
    r.sendline('Z')
    r.sendline('-1' if a2e_vals[i][0] == 'Z' else '1')
    
    r.recvuntil('to Bob, do you want to intercept (y/N)?')
    r.sendline('y') # a->e correctness
    r.sendline('Z')
    r.recvuntil('measured ')
    val = int(r.recvuntil('\n'))
    if val == 1:
        a2e_correct_idxs.append(i)
    
    r.sendline('y') # send correctness stuff back to b
    r.sendline('Z')
    if b_guessed_basis == 'Z': # our basis is always Z
        e2b_correct_idxs.append(i)
        r.sendline('1')
    else:
        r.sendline('-1')

print "Got correct a2e idxs", a2e_correct_idxs
print "Got correct e2b idxs", e2b_correct_idxs

# B takes every other measurement he made and sends it to Alice to verify. 
for i in range(0, min(len(e2b_correct_idxs), len(a2e_correct_idxs)), 2):
    r.sendline('y') # b->a, sending measured values
    r.sendline('Z')
    
    r.sendline('y') # replace value going to A with our collected info
    r.sendline('Z')
    r.sendline(str(a2e_vals[a2e_correct_idxs[i]][1]))
    
    r.sendline('y') # a->b ACK
    r.sendline('Z')
    r.sendline('n')

for i in range(0, min(len(e2b_correct_idxs), len(a2e_correct_idxs)), 2):
    r.recvuntil('to Alice, do you want to intercept (y/N)?')
    r.recvuntil('measured ')
    recvd_val = int(r.recvuntil('\n'))
    assert recvd_val == -1 # the qubit we share with B is always -1|Z>
    r.recvuntil('to Bob, do you want to intercept (y/N)?')
    r.recvuntil('measured ')
    assert int(r.recvuntil('\n')) == 1 # verify a says our qubits are correct

# one of the two channels (a->m or m->b) has finished

from Crypto import Random
from Crypto.Cipher import AES

if len(e2b_correct_idxs) < len(a2e_correct_idxs):
    # At this point, bob has fully setup the keypair with us

    r.recvuntil('classical message (')
    b_msg = r.recvuntil(')')[:-1]

    e_k = 0
    for i in e2b_correct_idxs[1::2][:128]:
        e_k <<= 1
        e_k |= 0 if e2b_vals[i][1] == -1 else 1

    e_aes = AES.new(hex(e_k)[2:].decode('hex'), AES.MODE_ECB, Random.new().read(32))
    print e_aes.decrypt(b_msg.decode('hex'))

    # now we need to finish off the connection with alice

    r.sendline('y')
    r.sendline('Z')
    r.sendline(str(a2e_vals[a2e_correct_idxs[i+1]][1]))
    
    # TODO because we already have the 1st half of the flag

else:
    # alice has a full keypair
    
    r.recvuntil('classical message (')
    msg = r.recvuntil(')')[:-1]
    r.sendline('n')

    aes_k = 0
    for i in a2e_correct_idxs[1::2][:128]:
        aes_k <<= 1
        aes_k |= 0 if a2e_vals[i][1] == -1 else 1

    a_aes = AES.new(hex(aes_k)[2:].decode('hex'), AES.MODE_ECB, Random.new().read(32))
    print a_aes.decrypt(msg.decode('hex'))
    
    for i in range(0, len(e2b_correct_idxs) - min(len(e2b_correct_idxs), len(a2e_correct_idxs)), 2):
        r.recvuntil('to Alice, do you want to intercept (y/N)?')
        r.sendline('n') # don't intercept
        r.recvuntil('do you want to send a qubit to Bob anyway')
        r.sendline('y') # alice respond even though connection abort? yes, fake the ACK
        r.sendline('Z')
        r.sendline('1')
    
    r.interactive()

# PCTF{perhaps_secrecy_aint_the_same_thing_as_authentication}