from pwn import *
import string

blocks = ['flag{', '', '']

charset = string.ascii_letters + string.digits + '_'

with remote('chal1.swampctf.com', 1450) as p:
    for b in range(3):
        for _ in range(len(blocks[b]), 16):
            for char in charset:
                flag_guess = blocks[b] + char
                thing = 'A' * (16 * (2-b) - len(flag_guess)) + flag_guess + 'A'*(16-len(flag_guess))
                p.sendline(thing)
                resp = p.recvline().strip().decode('hex')
                if resp[b*16:(b+1)*16] == resp[32:48]:
                    blocks[b] += char
                    print(''.join(blocks))
                    break
