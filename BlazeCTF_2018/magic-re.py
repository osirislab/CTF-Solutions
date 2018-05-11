from pwn import *
import subprocess

e = ELF('./magic')

regs = ['EDI', 'ESI', 'EBP', 'ESP', 'EBX', 'EDX', 'ECX', 'EAX']

last_msg = "AAAABAAACAAADAAAEAAAFAAAGAAAHAAA"

out = "pop ESI;"

for i in range(1, 48):
    stack = e.string(e.u32(e.symbols['r'] + (i*8 - 4)))
    msg = e.string(e.u32(e.symbols['r'] + (i*8)))
    next_stack = e.string(e.u32(e.symbols['r'] + (i*8 + 4)))

    # pushes don't modify msg
    if len(next_stack) > len(stack):
        pushed_val = next_stack[:4]
        idx = msg.find(pushed_val)
        if idx == -1:
            idx = 3 # ESP
        else:
            assert idx % 4 == 0
            idx /= 4
        out += "push "+regs[idx]+";"
        continue
    
    for j in range(0, 8*4, 4):
        if msg[j:j+4] != last_msg[j:j+4]:
            reg = regs[j/4]
            op = ""
            
            if len(next_stack) < len(stack):
                op = "pop "+reg+";"
            else:
                old_val = u32(last_msg[j:j+4])
                new_val = u32(msg[j:j+4])
                if new_val < old_val:
                    op = "dec "+reg+";"
                else:
                    op = "inc "+reg+";"
            
            last_msg = msg
            out += op
            break
    else:
        print hex(e.symbols['r'] + (i*8))

stuff = subprocess.check_output(['rasm2', '-b', '32', out])
print stuff.strip().decode('hex')