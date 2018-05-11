from pwn import *

context.log_level = 'debug'

#p = process('./NNawkward_pilgrim')
p = remote('chal1.swampctf.com', 1900)

p.recvuntil('bias\n')

def reset():
    p.sendline('1')
    p.recvuntil('bias\n')

def speak():
    p.sendline('2')
    res = p.recvline()
    p.recvuntil('bias\n')
    return res

def edit_weights(weights):
    p.sendline('3')
    p.sendline('')
    for row in weights:
        for w in row:
            p.recvline()
            p.sendline(str(w))

    p.recvuntil('bias\n')

def edit_bias(bias):
    p.sendline('4')
    p.sendline()
    for layer in bias:
        for node_b in layer:
            p.recvline()
            p.sendline(str(node_b))

    p.recvuntil('bias\n')

reset()
edit_weights([[0.13,0.01,0.183,0.315]]*4)

p.interactive()
