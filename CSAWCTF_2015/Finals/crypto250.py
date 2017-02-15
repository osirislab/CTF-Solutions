import prob, time, socket

s = socket.socket()
s.connect(('52.91.89.84', 4000))

s.recv(1000)

s1 = '\x80' + '\x00'*15

s.send(s1 + '\n')

s.recv(16)

first = s.recv(32).decode('hex')
print 'first message mac: ',repr(first)

s.recv(1000)

sec = '\x80' + '\x00'*15 + '\x80' + '\x00' * 15 + prob.xor(first, '\x80' + '\x00' * 15)

s.send(sec + '\n')

s.recv(100)

s.send(first.encode('hex') + '\n')

print s.recv(1000)