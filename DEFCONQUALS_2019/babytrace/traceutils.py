# Constraints:
def input_constraint_unconstrained(r, name, length):
    r.recvuntil("Choice: ")
    r.sendline("1")
    r.sendline(name)
    r.sendline(str(length))

def input_constraint_constrained(r, name, value):
    r.recvuntil("Choice: ")
    r.sendline("2")
    r.sendline(name)
    r.sendline(value)

def input_constraint_constant(r, value):
    r.recvuntil("Choice: ")
    r.sendline("3")
    r.sendline(value)


# Commands:
def start_trace(r):
    r.recvuntil("Choice: ")
    r.sendline("1")

def run_trace(r):
    r.recvuntil("Choice: ")
    r.sendline("0")

def step_trace(r, count):
    r.recvuntil("Choice: ")
    r.sendline("1")
    r.sendline(str(count))

def make_concrete(r, name):
    r.recvuntil("Choice: ")
    r.sendline("5")
    r.sendline(name)

def make_symbolic(r, name):
    r.recvuntil("Choice: ")
    r.sendline("6")
    r.sendline(name)

def show_constraints(r):
    r.recvuntil("Choice: ")
    r.sendline("7")
    r.recvuntil("CONSTRAINTS")
    print("\nCONSTRAINTS: " + r.recvline())
    r.recvuntil("Done.\n")
