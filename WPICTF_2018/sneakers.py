from pwn import *
context.log_level = 'debug'

braille = {
    '235': '!',
    '236': '?',
    '': ' ',
    '3': '\'',
    '36': '-',
    '1': 'a',
    '12': 'b',
    '14': 'c',
    '145': 'd',
    '15': 'e',
    '124': 'f',
    '1245': 'g',
    '125': 'h',
    '24': 'i',
    '245': 'j',
    '13': 'k',
    '123': 'l',
    '134': 'm',
    '1345': 'n',
    '135': 'o',
    '1234': 'p',
    '12345': 'q',
    '1235': 'r',
    '234': 's',
    '2345': 't',
    '136': 'u',
    '1236': 'v',
    '2456': 'w',
    '1346': 'x',
    '13456': 'y',
    '1356': 'z',
    '3456': '#',
    '2': ',',
    '23': ';',
    '25': ':',
    '256': '.',
}

rev = {v: k for k,v in braille.items()}

def dec():
    msg = ''
    a = r.recvline(False)
    b = r.recvline(False)
    c = r.recvline(False)
    r.recvline()
    a = [a[i:i+2] for i in range(0, len(a), 2)[::2]]
    b = [b[i:i+2] for i in range(0, len(b), 2)[::2]]
    c = [c[i:i+2] for i in range(0, len(c), 2)[::2]]
    for x,y,z in zip(a,b,c):
        d = ''
        if x[0] == '1':
            d+='1'
        if y[0] == '1':
            d+='2'
        if z[0] == '1':
            d+='3'
        if x[1] == '1':
            d+='4'
        if y[1] == '1':
            d+='5'
        if z[1] == '1':
            d+='6'
        msg += braille.get(d, d)
    return msg

def resp(r, c, pos):
    if pos in rev[c]:
        r.send('1')
    else:
        r.send('0')

def send_msg(r, m):
    for c in m:
        if 0x41 <= ord(c) <= 0x5a:
            r.send('00')
        resp(r, c.lower(), '1')
        resp(r, c.lower(), '4')
    r.send('x')
    for c in m:
        if 0x41 <= ord(c) <= 0x5a:
            r.send('00')
        resp(r, c.lower(), '2')
        resp(r, c.lower(), '5')
    r.send('x')
    for c in m:
        if 0x41 <= ord(c) <= 0x5a:
            r.send('01')
        resp(r, c.lower(), '3')
        resp(r, c.lower(), '6')
    r.sendline('x')

with remote('sneakers.wpictf.xyz', 31337) as r:
    msg = ''
    for _ in range(19):
        msg += dec()

    print(msg)
    send_msg(r, 'continue')

    msg = ''
    for _ in range(11):
        msg += dec()
    print(msg)

    send_msg(r, '#h#d#c#g#b')

    msg = ''
    for _ in range(8):
        msg += dec()
    print(msg)

    send_msg(r, 'ACCESS FLAG!')

    msg = ''
    for _ in range(5):
        msg += dec()
    print(msg)
