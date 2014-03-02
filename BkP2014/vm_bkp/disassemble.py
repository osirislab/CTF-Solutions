from sys import argv



def decode(insns):
	prev=None
	ret=[]
	for i,count in zip(map(ord,insns),range(len(insns))):
		if prev==None:
			prev=i
			ret.append(i)
			continue
		decoded_byte=(i^prev)^(count%11)
		ret.append(decoded_byte)
		prev=i
	return ''.join(map(chr,ret))

def disassemble(insns):
	i_len=len(insns)
	while len(insns)>4:
		addr=i_len-len(insns)
		print '{}'.format(hex(addr)),
		curr=insns.pop(0)
		if curr==0x50:
			imm=insns.pop(0)
			print 'PUSH {} {} {}'.format(hex(imm),chr(imm),imm)
		elif curr==0x6e:
			print 'PUSH 0'
		elif curr==ord('+'):
			imm=insns.pop(0)
			print 'ADD  {} {}'.format(hex(imm),imm)
		elif curr==ord('-'):
			imm=insns.pop(0)
			print 'SUB  {} {}'.format(hex(imm),imm)
		elif curr==0x4e:
			print 'NOP'
		elif curr==0x4f:
			print 'OPEN'
		elif curr==0x52:
			print 'STK_RST'
		elif curr==0x5f:
			print 'hlt0'
		elif curr==0x61:
			imm=insns.pop(0)
			print 'SNIBBLE_SWAP {}'.format(imm)
		elif curr==0x67:
			print 'READ \t\t[++sp]=fgetc(file)'
		elif curr==0x69:
			print 'NOT'
		elif curr==0x6a:
			imm=insns.pop(0)
			print 'JMP +{} {}'.format(hex(imm),hex(addr+imm+2))
		elif curr==0x6b:
			imm=insns.pop(0)
			print 'JE +{} {}'.format(hex(imm),hex(addr+imm+2))
		elif curr==0x6c:
			imm=insns.pop(0)
			print 'JNE +{} {}'.format(hex(imm),hex(addr+imm+2))
		elif curr==0x70:
			print 'PRINT'
		elif curr==0x71:
			print 'NIBBLE_SWAP'
		elif curr==0x72:
			print 'REVERSE'
		elif curr==0x73:
			imm=insns.pop(0)
			print 'SSWAP {} {} \t\t[sp]<->[sp-imm]'.format(hex(imm), imm)
		elif curr==0x74:
			imm=insns.pop(0)
			print 'FLIP_BIT {} {}'.format(hex(imm),imm)
		elif curr==0x78:
			imm=insns.pop(0) #xor
			print 'XOR {}'.format(hex(imm))
		elif curr==0x51:
			print 'POP'
		elif curr==ord('D'):
			dword=0
			i1=insns.pop(0)
			dword+=i1
			i2=insns.pop(0)
			dword+=i2<<8
			i3=insns.pop(0)
			dword+=i3<<16
			i4=insns.pop(0)
			dword+=i4<<24
			print 'AES {}'.format(hex(dword))
		elif curr==ord('='):
			imm=insns.pop(0)
			print 'EQ {} {} {}'.format(hex(imm),chr(imm),imm)
		else:
			print 'UNKNOWN {} {} {}'.format(hex(curr),chr(curr),curr)

offset=0
adjust=0

if len(argv)>3:
	filename=argv[1]
	offset=int(argv[2])
	adjust=int(argv[3])
if len(argv)>2:
	filename=argv[1]
	offset=int(argv[2])
elif len(argv)>1:
	filename=argv[1]

else:
	print 'give file'

insns=file(filename).read()[offset:]
decoded_insns=map(ord,decode(insns))
disassemble(decoded_insns)






