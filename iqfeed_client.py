############################
# TCP client
############################

import socket
import sys



# connect socket to port where server is listening
server_host = "LENOVO"
server_port = 1234
server_address = (server_host, server_port)
#print >>sys.stderr, 'connecting to %s port $s' % server_address



# for each SYM in queue
syms = ["DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII","DDD","ADBE","XXII"]

# download each symbol to disk
for sym in syms:

    print "Getting %s" % sym

    print "Connecting to %s port %s" % server_address

    try:
        # create TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
    except Exception, e:
        print "Could not connect"
        print "Exception type is %s" % e
    else:
        print "Connected OK"



        while (1) :

            # message to send
            #message = raw_input("SYM? ")
            #sock.sendall(message)


            sock.sendall(sym)

            buffer = ""
            data = ""

            while True:
                data = sock.recv(4096)
                buffer += data

                # check if the end message string arrives
                if "!ENDMSG!" in buffer:
                    break

            print >> sys.stderr, 'closing sockets'
            sock.close

            # remove the end message string
            buffer = buffer[:-12]
            print buffer

            break



