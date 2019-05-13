#!/usr/bin/env python2

import pwn
from traceutils import *


remote = False
flag = ""
last_char = ""
index = 16


if remote:
    r = pwn.remote("mamatrace.quals2019.oooverflow.io", 5000)
else:
    r = pwn.process("./pitas.py")

# Header
r.recvuntil("# Are you ready for the PITA?\n\n")


# def flagleak():
    # # Binary select
    # r.recvuntil("Choice: ")
    # if remote:
    #     r.sendline("2")
    # else:
    #     r.sendline("1")

    # start_trace(r)

    # # input_constraint_constant(r, '09' + 'ff'*7)
    # input_constraint_constrained(r, "input", '09')
    # input_constraint_constant(r, 'ff'*7)

    # # input_constraint_constrained(r, "r12d_52_32", '0a')
    # # input_constraint_constrained(r, "r12b_52_8", "09")
    # # input_constraint_constrained(r, "r12d_53_32", "10")
    # # input_constraint_constrained(r, "r12d", format(9, '016x'))

    # # Write to input buffer memory
    # # input_constraint_constrained(r, format(0x07fffffffffefe40, '016x'), format(index, '08x'))
    # # input_constraint_constrained(r, "0x07fffffffffefe40", format(index, '08x'))

    # # add input constraint for rbx way ahead of time
    # # input_constraint_constrained(r, "reg_rbx_43_64", format(10, '016x'))
    # # input_constraint_constrained(r, "rbx_51_64", format(10, '016x'))
    # # RBP in loop: rbp_52_64

    # run_trace(r)

    # step_trace(r, 12)
    # # make_symbolic(r, "r12b")
    # # make_concrete(r, "r12b")

    # # step_trace(r, 2)

    # # make_symbolic(r, "r12b")
    # # make_symbolic(r, "eax")

    # # step_trace(r, 1)

    # show_constraints(r)

    # r.interactive()


def headerquery2():
    # Binary select
    r.recvuntil("Choice: ")
    r.sendline("3")

    start_trace(r)

    # input_constraint_constrained(r, "input", '0c000080')
    # input_constraint_unconstrained(r, "input", 1)
    # input_constraint_constant(r, '0000')
    input_constraint_constant(r, '00000000')
    input_constraint_constrained(r, "0x7fffffffffefe39", 'ffffffffff')

    # input_constraint_constrained(r, 'eax_53_32', '02000000')

    run_trace(r)

    # Load one
    step_trace(r, 9)

    # Load two
    # step_trace(r, 1)
    # make_symbolic(r, "eax")

    # eax_52_32

    # Load three
    pass

    # input_constraint_constrained(r, 'eax_52_32', '00000004') # ?
    # input_constraint_constrained(r, 'eax_53_32', '00000004') # ?
    # input_constraint_constrained(r, 'eax_54_32', '04000004') # ?

    # step_trace(r, 13) # 0x40085a - input to input buffer x1

    # make_symbolic(r, "eax") # ?
    # show_constraints(r) # ?
    # step_trace(r, 1) # ?

    # make_symbolic(r, "eax") # ?
    # show_constraints(r) # ?
    # step_trace(r, 3) # ?
    # show_constraints(r) # ?

    # step_trace(r, 0) # ?

    show_constraints(r)
    r.interactive()

# flagleak()
headerquery2()