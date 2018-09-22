import os
import sys
import time
import socket

# choose a file to serve
filename = "C:\\Users\\lenovoguest\\Documents\\devsh\\data\\weblogs\\2013-09-16.log"

print(os.path.isfile(filename))

# now that we have a file, let's open it
#file_object = open (pathToFile)

# and print out its content
# for line in file_object :
#     print line

host = "LENOVO"
port = 1234
sleeptime = 1 / 20



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(1)

while (1):
    print "Waiting for connection on", host, ":", port
    (clientsocket, address) = serversocket.accept()

    print "Connection from", address

    data = clientsocket.recv(1024)

    clientsocket.sendall(data)
