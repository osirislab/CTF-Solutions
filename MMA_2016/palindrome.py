import itertools
from pwn import remote

r = remote('ppc1.chal.ctf.westerns.tokyo', 31111)

r.recvuntil('Input: ')

while True:
	print r.recvuntil('Input: ')
	inp = r.recvline().strip().split(' ')
	print inp
	r.recvuntil('Answer: ')

	if int(inp[0]) < 11:
		print "Brute-forcing..."
		for p in itertools.permutations(inp[1:]):
			s = ''.join(p)
			if s == s[::-1]:
				print p
				r.sendline(' '.join(p))
				break

print r.recv()