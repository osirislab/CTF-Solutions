from pwn import *

r = remote('macsh.chal.pwning.xxx', 64791)
r.recvuntil('> ')

ls_blk = 'echo AAAAAAAAAAA'
len_blk = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
pad_blk = '\x10'*16
a_blk = 'A'*16

entered_len_blk = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00'

m1 =    entered_len_blk + pad_blk + a_blk + (a_blk*(16*8 - 3))
m1+=    ls_blk          + len_blk + a_blk + (a_blk*(16*8 - 3))

r.sendline('<|>tag '+ls_blk)
echo_len_pad = r.recvline().strip().decode('hex')
print(echo_len_pad)
r.recvuntil('> ')

r.sendline('<|>tag '+m1)
echo_len = r.recvline().strip().decode('hex')
print(echo_len)
r.recvuntil('> ')

def xor(x,y):
    return ''.join(chr(ord(a)^ord(b)) for a,b in zip(x,y))

pad = xor(echo_len_pad, echo_len)

ls_blk = 'cat ././flag.txt'

m1 =    entered_len_blk + pad_blk + a_blk + (a_blk*(16*8 - 3))
m1+=    ls_blk          + len_blk + a_blk + (a_blk*(16*8 - 3))

r.sendline('<|>tag '+m1)
ls_len = r.recvline().strip().decode('hex')
print(ls_len)
r.recvuntil('> ')

ls_len_pad = xor(ls_len, pad)
print(ls_len_pad)
r.sendline(ls_len_pad.encode('hex') + '<|>' + ls_blk)

r.interactive()
