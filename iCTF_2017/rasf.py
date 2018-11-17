from pwn import *
import itertools
from z3 import BitVec, BitVecVal, Solver, If, simplify, Concat, Extract, And, Or, LShR, UDiv, sat, Int
from ictf import iCTF
from multiprocessing import Pool
i = iCTF()
team = i.login('nmg355@nyu.edu', 'HZBrKynG4XAMvWPa')

BVV = BitVecVal
BV = BitVec

int128 = lambda x: Concat(BVV(0, 64), x)
int64 = lambda x: Extract(63, 0, x)

def weird_op(x):
    k = x - (1337331 * LShR(int64(LShR(0x0C8B98A756AA1D561 * int128(x), 64)), 20))
    return int64(k)

def choose_op(a1, a2, op):
    r = If(op == 0,
            a2 + a1,
            If(op == 1,
                a1 - a2,
                If(op == 2,
                    a2 * a1,
                    If(op == 3 and a2 != 0,
                        UDiv(a1, a2),
                        False
                    )
                )
            )
    )
    return r

def all_choices():
    choices = (0, 1, 2, 3)
    return list(itertools.product(choices, choices, choices))

def solve_for(inps):
    r1, r2, r3, r4, v11 = [BVV(x, 64) for x in map(int, inps.split(', '))]
    print r1, r2, r3, r4, v11

    for choice1, choice2, choice3 in all_choices():
        v6 = choose_op(r1, r2, choice1)
        v6_1 = choose_op(v6, r3, choice2)
        v6_2 = choose_op(v6_1, r4, choice3)

        if simplify(weird_op(v6_2)) == v11:
            return choice1, choice2, choice3

def exploit(t):
    target = lambda: remote(t['hostname'], t['port'], timeout=3)

    try:
        with target() as s:
            n_inputs = int(s.recvline().strip())
            for _ in range(n_inputs):
                inp = s.recvline().strip()
                c1, c2, c3 = solve_for(inp)
                s.sendline('{} {} {}'.format(c1, c2, c3))

            s.recvuntil("want?:")
            s.send("2\n3\n19\n"+t['flag_id']+"\n16\n"+"A"*16+"\n0\n")
            s.recvuntil("GameTime:")
            v19_c, v20_c, x_c, v22_c, v23_c, y_c = map(int, s.recv().split(', '))
            solv = Solver()
            v18 = Int('v18')
            v21 = Int('v21')
            v19 = Int('v19')
            solv.add(v19 == v19_c)
            v20 = Int('v20')
            solv.add(v20 == v20_c)
            v22 = Int('v22')
            solv.add(v22 == v22_c)
            v23 = Int('v23')
            solv.add(v23 == v23_c)
            x = Int('x')
            solv.add(x == x_c)
            solv.add(x == v19*v18 + v20*v21)
            y = Int('y')
            solv.add(y == y_c)
            solv.add(y == v22*v18 + v21*v23)

            solv.check()
            solv.model()

            s.sendline(str(solv.model()[v18].as_long()))
            s.sendline(str(solv.model()[v21].as_long()))
            s.recvuntil("log:")
            s.send("15\n:83xkHFchNObsWf\n")
            s.recvuntil("):")
            s.sendline("478175")
            s.recvuntil("Name:")
            magic = s.recvuntil(":")[:-1]

        with target() as s:
            n_inputs = int(s.recvline().strip())
            for _ in range(n_inputs):
                inp = s.recvline().strip()
                c1, c2, c3 = solve_for(inp)
                s.sendline('{} {} {}'.format(c1, c2, c3))

            s.recvuntil("want?:")
            s.send("2\n5\n19\n"+t['flag_id']+"\n16\n"+magic+"\n")
            s.recvline()
            flag = s.recvline().strip()

        return flag

    except:
        return

p = Pool(3)

while True:
    flags = []
    targets = team.get_targets(service='rasf')['targets']
    flags = p.map(exploit, targets)
    flags = filter(None, flags)

    print flags
    while True:
        try:
            print team.submit_flag(flags)
            break
        except Exception as e:
            print 'got',e,'retrying in 1s'
            time.sleep(1)
    time.sleep(team.get_tick_info()['approximate_seconds_left'] + 30)
