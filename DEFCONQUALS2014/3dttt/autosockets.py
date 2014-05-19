import sys
import os
import re
import time

import socket as _socket
from socket import AF_INET, AF_INET6, SOCK_STREAM, SOCK_DGRAM

try: 
    from socket import AF_UNIX
except ImportError:
    # AF_UNIX only available on UNIX. :O
    pass

try: 
    from pebble import thread
except ImportError:
    print "Threading decorator unavailable. Install pebble with sudo pip install pebble"

class print_hook:
    """ Dirty hack for overriding default print behavior """
    def __init__(self, *writers) :
    	self.writers = writers
    	
    def write(self, text):
        for w in self.writers :
            if text != '\n':
                if len(text) > 0 and text[-1] == '\n':
                     w.write("[DEBUG] " + text)
                     return
                w.write("[DEBUG] " + text + "\n")

class error_hook:
    def __init__(self, *writers) :
    	self.writers = writers
    	
    def write(self, text):
        for w in self.writers :
            if text != '\n': 
                w.write("[ERROR] " + text + "\n")

sys.stdout = print_hook(sys.stdout)
#sys.stderr = error_hook(sys.stderr)

class listener:
    def __init__(self, port):
        HOST = ''
        PORT = 6969
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while 1:
            conn, addr = s.accept()
            self.interact(conn, addr)

    def interact(self, conn, addr):
        command = ''
        print "Received", addr

        while (command != 'exit'):
            command = raw_input('> ')
            conn.send(command + '\n')
            time.sleep(.5)
            data = conn.recv(0x10000)
            if not data:
                print "Disconnected", addr
                return
            print data.strip(),
        else:
            print "Disconnected", addr

class socket:
    def __init__(self, addr, port, timeout=2, stype=AF_INET, sproto=SOCK_STREAM):
        self.s = _socket.socket(stype, sproto)
        self.s.connect((addr, port))
        self.s.settimeout(timeout)

    def __getattr__(self, name, *args, **kwargs):
        func = getattr(self.s, name)
        return func

    def recv(self, regex=False, end='\n'):
        if type(regex) == int or type(regex) == long:
            return self.s.recv(regex)
        total=[]
        data='\n'
        while data != "":
            try: 
                data = self.s.recv(8192)
                if end in data:
                    total.append(data)
                    data = ""
                    break
                total.append(data)
                data = ""
            except _socket.error:
                break

        if regex:
           return re.findall(regex, ''.join(total))
        return ''.join(total)

    def send(self, text):
        self.s.sendall(text)
    
