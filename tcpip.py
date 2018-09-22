import os

# choose a file to manipulate
pathToFile = "C:\\2013-09-15.log"

print(os.path.isfile(pathToFile))

# now that we have a file, let's open it
file_object = open (pathToFile)

# and print out its content
# for line in file_object :
#
#     print line


############################
# TCP client
############################

import socket
import sys

# create TCP/IP socket
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

# connect socket to port where server is listening
server_address = ('horus.localdomain', 1234)
#print >>sys.stderr, 'connecting to %s port $s' % server_address

sock.connect(server_address)
while True :
    data = sock.recv(1024)
    #amount_received += len(data)
    print >>sys.stderr, 'received "%s"' % data