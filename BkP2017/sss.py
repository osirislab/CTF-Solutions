from pwn import *

#context.log_level = "DEBUG"

cmd = 'cat flag;'

for i in range(256):
    r = remote('54.202.2.54', 9876)
    #r = process('./sss')

    r.recvuntil('>_ ')

    #execute
    r.sendline('2')

    r.recvuntil('>_ ')
    
    # setup cmd
    test_cmd = cmd + chr(i)*(0xff-len(cmd))

    r.sendline(test_cmd)

    r.recvuntil('>_ ')

    #signature
    r.sendline('A'*40)

    try:
        print r.recv()
    except:
        continue
