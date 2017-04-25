#print f=open('share/flag');print ''.join(chr(reduce(lambda a,b:a^b,map(ord,f.read(65000)),0))for _ in range(99))

#$(python -c "K=65000;f=map(ord,open('/share/flag').read());print ''.join(chr(reduce(lambda a,b:a^b,f[k*i:(k*(i+1))],0)) for i in range(15))")

spoken = """50
43
54
46
7b
4c
31
35
73
74
33
6e
5f
54
30
5f
5f
72
65
65
65
5f
72
65
65
65
65
65
65
5f
72
65
65
65
5f
6c
61
7d"""

print ''.join(chr(x) for x in [int(x,16) for x in spoken.split('\n')])