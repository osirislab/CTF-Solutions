#!/usr/bin/python


#Evan Jensen
encrypted_key='RDBgbDVrb0t/MTJydFM7dUwna35SSS9gakUianQobCcl'

def transform1(s):
	ret=[]
	for i,c in zip(map(ord,s),range(len(s))):
		ret.append(chr(i^c))
	return ''.join(ret)

def transform2(s):
	ret=[]
	for i,c in zip(map(ord,s),range(len(s))):
		ret.append(chr(i-5%(c if c else 1)))
	return ''.join(ret)

print transform2(transform1(encrypted_key.decode('base64')))
