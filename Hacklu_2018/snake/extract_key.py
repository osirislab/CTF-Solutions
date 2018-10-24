import angr, claripy

p = angr.Project('Snake.exe', auto_load_libs=False)

key_chars = [claripy.BVS('key_%d' % i, 8) for i in range(16)]

def q_string(state):
    # set al = key_chars[r8]
    idx = state.solver.eval(state.regs.r8)
    state.regs.al = key_chars[idx]
    print idx
    print state.regs.al

p.hook(0x140004B87, q_string, length=0x140004B96-0x140004B87)
p.hook(0x140004BBC, q_string, length=0x140004BCB-0x140004BBC)

state = p.factory.blank_state(addr=0x140004B61)

# store len (16) into mem
state.memory.store(state.regs.r15 + 0x18, 0xdead0000)
state.memory.store(0xdead0000 + 0x4, 0x10)

simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x140004C17, avoid=0x140004C1E)

print (''.join(chr(simgr.one_found.solver.eval(c)) for c in key_chars)).encode('hex')
