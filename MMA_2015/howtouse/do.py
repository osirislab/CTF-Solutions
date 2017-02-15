set = open('data.txt','r').read().split("\n")
out = ['']*len(set)
esp = 0xb4
for e in set:
	if e == "push":
		esp -= 4
	elif e == "pop":
		esp += 4
	else:
		addr = int(e[4:e.index(" ")],16)
		chr = e[-1]
		dst = (esp-addr) / 4
		if out[dst] == '':
			out[dst] = chr
		else:
			print out
			print "Index {} already set".format(dst)

print ''.join(out)