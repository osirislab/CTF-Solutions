import base64, string
from hashlib import md5
from pwn import *

def xor_char(s, idx, xor):
    return s[:idx] + chr(ord(s[idx]) ^ xor) + s[idx+1:]

charset = string.ascii_letters + string.digits + '_'

flag = 'flag{Ev3n_dunge0send_modflag_encns_are_un5af3_wIth_'

while True:
    try:
        with remote('chal1.swampctf.com', 1460) as r:
            cipher = base64.b64decode(r.recvline().strip())
            mod_cipher = cipher
            for i, (pt_char, new_char) in enumerate(zip("end_modflag_enc", "get_modflag_md5")):
                mod_cipher = xor_char(mod_cipher, i+17, ord(pt_char) ^ ord(new_char))
            r.recvuntil('do?')
            r.sendline(base64.b64encode(mod_cipher))
            r.recvline()
            assert 'Dungeon' in r.recvline()

            for pad_val in range(1, 256):
                tmp = xor_char(cipher, len(cipher)-1, pad_val)
                r.sendline(base64.b64encode(tmp))
                md = base64.b64decode(r.recvline().strip())
                for char in charset:
                    if md == md5(flag + char).digest():
                        flag += char
                        print(flag)
                        break
    except AssertionError:
        continue
