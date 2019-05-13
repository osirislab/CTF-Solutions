#!/usr/bin/env python3

import claripy
import angr
import sys
import os

PROJECTS = { }
TRACES = { }
BINPATH = os.path.join(os.path.dirname(__file__), "bins")

def one_menu(items, done=True, default=None):
	choices = [ None ]
	for item in items:
		if type(item) in (str, bytes):
			print(item)
		else:
			print("%d <- %s" % (len(choices), item[0]))
			choices.append(item[1])
	if done:
		print("0 <- Done.")

	cstr = input("Choice: ")
	if not cstr:
		return default if default is not None else one_menu(items, done=done)

	choice = int(cstr)
	assert 0 <= choice < len(choices), "Invalid choice!"
	assert choice or done, "Invalid choice!"
	return choices[choice]

def menu(*items, do_while=False, loop=False, back=False, default=None):
	if do_while:
		yield True

	c = default
	while True:
		c = one_menu(items, done=back, default=c)
		if callable(c):
			yield c()
		elif c is None:
			break
		else:
			yield c

		if not loop:
			break

def load_binary(binary):
	print("Loading binary %s..." % binary)
	if binary not in PROJECTS:
		assert os.path.exists(binary), "Somehow chose a nonexistent binary?"
		p = angr.Project(binary)
		PROJECTS[binary] = p
		TRACES[binary] = [ ]
	p = PROJECTS[binary]

	for _ in menu(
		"What would you like to do?",
		("Start a trace.", lambda: start_trace(binary)),
		("Resume a trace.", lambda: resume_trace(binary)),
		("Delete a trace.", lambda: delete_trace(binary)),
		do_while=True, loop=True, back=True
	):
		print("Traces:")
		for n,t in enumerate(TRACES[binary]):
			print("%d: %s" % (n, t.one_active))

def start_trace(binary):
	p = PROJECTS[binary]
	s = p.factory.full_init_state(stdin=angr.SimFileStream, chroot=BINPATH, concrete_fs=True)

	def add_unconstrained():
		stdin_name = input("Variable name: ")
		stdin_len = int(input("Variable length (in bytes): "))
		stdin_var = claripy.BVS(stdin_name, stdin_len*8, explicit_name=True)
		s.posix.stdin.write(None, stdin_var)

	def add_constrained():
		stdin_name = input("Variable name: ")
		stdin_str = bytes.fromhex(input("Variable contents (in hex): "))
		stdin_len = len(stdin_str)
		stdin_var = claripy.BVS(stdin_name, stdin_len*8, explicit_name=True)

		# print("stdin_name ", stdin_name)
		# print("stdin_str ", stdin_str)
		# print("stdin_len ", stdin_len)
		# print("stdin_var ", stdin_var)
		# print("stdin_var == stdin_str")

		s.posix.stdin.write(None, stdin_var)
		s.add_constraints(stdin_var == stdin_str)

	def add_concrete():
		stdin_str = bytes.fromhex(input("Value (in hex): "))
		stdin_var = claripy.BVV(stdin_str)
		s.posix.stdin.write(None, stdin_var)

	for _ in menu(
		"Input specification.",
		("Add unconstrained symbolic variable.", add_unconstrained),
		("Add constrained symbolic variable.", add_constrained),
		("Add concrete value.", add_concrete),
		do_while=True, loop=True, back=True
	):
		print("Current size of input: %d" % s.solver.eval(s.posix.stdin.pos))

	s.posix.stdin.pos = 0
	s.posix.stdin.has_end=True
	assert s.solver.satisfiable(), "Unexpected unsat state."

	simgr = p.factory.simulation_manager(s)
	simgr.explore(find=p.loader.find_symbol('main').rebased_addr).move('found', 'active')
	assert len(simgr.active) == 1

	TRACES[binary].append(simgr)
	resume_trace(binary, trace=len(TRACES)-1)

def resume_trace(binary, trace=None):
	if trace is None:
		choice = next(menu(
			"Which trace?",
			*[ (str(t.one_active), i) for i,t in enumerate(TRACES[binary]) ],
			do_while=False, loop=False, back=False
		))
		simgr = TRACES[binary][choice]
	else:
		simgr = TRACES[binary][trace]

	def step():
		num_steps = int(input("How many steps: "))
		for _ in range(num_steps):
			simgr.step()
			if simgr.deadended and not simgr.active:
				print("The path has deadended!")
				print("STDIN:",  simgr.one_deadended.posix.dumps(0))
				print("STDOUT:", simgr.one_deadended.posix.dumps(1))
				print("STDERR:", simgr.one_deadended.posix.dumps(2))
				print("Goodbye!")
				sys.exit(0)
			assert len(simgr.active) == 1, "This is a tracing interface, not a general symbolic exploration client!!!"

	def symbolize_register():
		rn = input("Register name? ")
		rv = simgr.one_active.registers.load(rn)
		sv = claripy.BVS(rn, rv.size())
		simgr.one_active.registers.store(rn, sv)
		simgr.one_active.add_constraints(rv == sv)

	def concretize_register():
		rn = input("Register name? ")
		rv = simgr.one_active.solver.eval(simgr.one_active.registers.load(rn))
		# print("rn ", rn)
		# print("rv ", rv)
		simgr.one_active.registers.store(rn, rv)

	def embed():
		import ipdb; ipdb.set_trace()

	for _ in menu(
		"What do?",
		("Step", step),
		("Dump stdin", lambda: print("STDIN:", simgr.one_active.posix.dumps(0))),
		("Dump stdout", lambda: print("STDOUT:", simgr.one_active.posix.dumps(1))),
		("Dump stderr", lambda: print("STDERR:", simgr.one_active.posix.dumps(2))),
		("Concretize register", concretize_register),
		("Symbolize register", symbolize_register),
		("Print constraints", lambda: print("CONSTRAINTS:", simgr.one_active.solver.constraints)),
		#("Shell", embed),
		do_while=False, loop=True, back=True
	):
		print("Current binary: %s" % binary)
		print("Current trace: %s" % simgr.one_active)

def delete_trace(binary):
	if len(TRACES[binary]) == 0:
		print("No traces!")
		return

	choice = next(menu(
		"Which trace?",
		*[ (str(t), i) for i,t in enumerate(TRACES[binary]) ],
		do_while=False, loop=False, back=False
	))
	del TRACES[binary][choice]

def main():
	print("#"*79)
	print("#"*79)
	print("#"*79)
	print("#"*67 + "#### WELCOME")
	print("#"*67 + "######### TO")
	print("#"*67 + "######## THE")
	print("#"*67 + "#### PROGRAM")
	print("#"*67 + " INTERACTIVE")
	print("#"*67 + "#### TRACING")
	print("#"*67 + "####### AS A")
	print("#"*67 + "### SYMBOLIC")
	print("#"*67 + "#### SERVICE")
	print("#"*79)
	print("#"*79)
	print("#"*79)
	print("")
	print("        %%%%%%    %%%   %%%%%%%    %     %%%%%   %%%%%          ")
	print("        %     %    %       %      % %   %     % %     %         ")
	print("        %     %    %       %     %   %  %       %               ")
	print("        %%%%%%     %       %    %     %  %%%%%   %%%%%          ")
	print("        %          %       %    %%%%%%%       %       %         ")
	print("        %          %       %    %     % %     % %     %         ")
	print("        %         %%%      %    %     %  %%%%%   %%%%%          ")
	print("")
	print("This service empowers the everyhacker to utilize the cutting-edge angr")
	print("binary analysis framework! Fear not: though angr is daunting, this service")
	print("scopes the challenge to the use of angr purely for symbolic tracing.")
	print("Don't be scared!")
	print("")
	print("# Greetz")
	print("")
	print("It is important to stress that we stand on the shoulders of giants [1,2,3,4].")
	print("Much of angr's design, implementation, and optimization was inspired by")
	print("the insights in those papers. Anyone interested in the functionality,")
	print("implications, and failure modes of symbolic execution should read those")
	print("papers.")
	print("")
	print("[1] KLEE: Unassisted and Automatic Generation of High-Coverage Tests")
	print("    for Complex Systems Programs")
	print("[3] Billions and Billions of Constraints: Whitebox Fuzz Testing in Production")
	print("[4] Unleashing MAYHEM on Binary Code")
	print("[5] Enhancing Symbolic Execution with Veritesting")
	print("")
	print("# Are you ready for the PITA?")
	print("")


	all(True for _ in menu(
		*[ "Which binary do you want to trace?" ] +
		[ (b, lambda b=b: load_binary(os.path.join(BINPATH, b))) for b in sorted(os.listdir(BINPATH)) if os.access(os.path.join(BINPATH, b), os.X_OK) ],
		loop=True, back=True)
	)
	print("Goodbye!")

if __name__ == '__main__':
	try:
		main()
	except AssertionError as e:
		print("Assertion violation:", str(e))
		#raise
	except Exception as e:
		print("Something went wrong...", str(e))
		#raise
