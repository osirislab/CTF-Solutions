#!/usr/bin/env python

from socket import *
from MeasurementLib import *
import base64
import marshal
import thread
import types

flag = None  
cookie = None
flag_id = None

measurements = set([])

def connection_handler(clientsock,addr):
  try:
    clientsock.send("Welcome back. Please insert your measurement\n:")
    data = clientsock.recv(BUFSIZ)
    if not data: return
    r = calculate(data)
    if not r:
      ## Original code
      # if int(data.split(',')[-1]) == flag_id:
      #  clientsock.send("%s\n"%flag)
      # clientsock.close()
      ##
      ## Prevent backdoor to flag
      if int(data.split(',')[-1]) == flag_id:
        clientsock.close()
      ##
    else:  
      if data in measurements:
          clientsock.send("Thanks, but we have already seen this measurement\n")
          clientsock.close()
      else:
        measurements.add(data)
        clientsock.send("Floods ahead! Please enter your command\n:")
        data = clientsock.recv(BUFSIZ)  
        ## Prevent execution of user code by checking for expected function name     
        if "callback" in base64.b64decode(data):
          clientsock.close()
        ##
        types.FunctionType(marshal.loads(base64.b64decode(data)), globals(), "callback")(clientsock)
        clientsock.close()
  except Exception as e: print e
  return

if __name__ == "__main__":
  
  HOST = "0.0.0.0"
  PORT = 3333
  BUFSIZ = 1024
  ADDR = (HOST, PORT)
  serversock = socket(AF_INET, SOCK_STREAM)
  serversock.bind(ADDR)
  serversock.listen(2)

  while True:
    clientsock, addr = serversock.accept()
    thread.start_new_thread(connection_handler, (clientsock, addr))
  serversock.close()  
