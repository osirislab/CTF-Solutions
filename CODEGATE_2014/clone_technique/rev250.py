ek=[15, 142, 158, 57, 61, 94, 63, 168, 122, 104, 12, 61, 139, 173, 197, 208, 123, 9, 52, 182, 163, 160, 62, 103, 93, 214, 0, 0]



def ror(x, n):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (32 - n))


def rol(x, n):
    return ror(x, 32 - n)


def decrypt(i1, i2):
	dec=[]
	for a,b in zip(ek[::2],ek[1::2]):
		dec.append((i1&0xFF)^a)
		i1=rol(i1,5)^0x2F

		dec.append((i2&0xFF)^b)
		i2=rol(i2,11)^(i1&0xFF)

	return ''.join(map(chr,dec))




def mutate_on_start(a,b):
	a=a^0x0B72AF098
	b=(a*b)^b
	b%=2**32
	return a,b

def mutate_for_main(a,b):
	a_prime=0x1D*a 
	a_prime%=2**32
	a_prime+=7*pow(a,2,2**32)
	a_prime%=2**32
	b_prime=pow(a_prime^b, a_prime%2 + 5, 2**32)
	return a_prime,b_prime

all_values=[]
once=True

def mutate_for_run(a,b,run=None):
	if run==None:
		run=1

	all_values.append((a,b)) 
	a,b=mutate_on_start(a,b) #set gobals
	
	global once
	if once:
		print hex(a),hex(b)
		once=False
	global_a=a
	a,b=mutate_for_main(a,b) #modify locals

	if(global_a>0xD0000000):
		exit_value=(0xD * (a / 0x1B) )^ 0x1F2A990D
		exit_value%=2**32
		return exit_value
	if(run>400):
		return 0

	while run<=400:
		run+=1
		exit_value=mutate_for_run(a,b,run)
		a=exit_value
		b=pow(exit_value^b, exit_value%0x1E, 2**32)
		if exit_value==0:
			return 0
	

s1,s2=(0xA8276BFA,
	   0x92F837ED)

mutate_for_run(s1,s2)

print len(all_values)

for a,b in all_values:
	d=decrypt(a,b)
	if all([i<0x80 for i in map(ord,d[:-5])]):
		print d

"""
for a,b in all_values:
	d= decrypt(a,b)
	print d
"""
