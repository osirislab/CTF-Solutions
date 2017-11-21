import angr

p = angr.Project('./4TRUN', auto_load_libs=False)

# NOP out gfortran stuff
p.hook(0x4007e0, lambda s: None)
p.hook(0x400830, lambda s: None)
p.hook(0x4007f0, lambda s: None)

p.hook(0x400840, lambda s: None)
p.hook(0x400800, lambda s: None)
p.hook(0x400850, lambda s: None)

state = p.factory.blank_state(addr=0x40097a)

for i in range(36):
    state.mem[state.regs.rbp-0x90 + i:].byte = state.solver.BVS('flag', 8)

pg = p.factory.simgr(state, threads=2)
ex = pg.explore(find=0x4014a4, avoid=(0x4013f7,))

f = ex.found[0]

print f.solver.eval(f.memory.load(f.state.regs.rbp-0x90, 36), cast_to=str)
