import sys
import socket

if __name__ == "__main__":

    ######################################
    # server socket
    ######################################

    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host,
    # and a 1000+ port
    #host = socket.gethostname()
    host = "LENOVO"
    port = 4321
    serversocket.bind((host, port))

    # become a server socket
    serversocket.listen(5)



    # accept connection from client
    print "\nWaiting for connection on", host, ":", port, ".......\n"
    (clientsocket, client_address) = serversocket.accept()


    print "Connection accepted from {}.".format(client_address)

    print "Connecting to live feed......."

    # define (iqfeed client) server host, port and symbols to download
    host = "127.0.0.1"
    port = 5009  # live:5009 - hist:9001 - admin:9003

    # Open a streaming socket to the IQFeed server locally
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    print "Connected to feed."

    print "Setting up connection......."

    # set protocol to 6 to watch trades only
    message = "S,SET PROTOCOL,6.0\n"
    sock.sendall(message)


    # request all fieldnames
    message = "S,REQUEST ALL UPDATE FIELDNAMES\n"
    sock.sendall(message)


    # request current fieldnames
    message = "S,REQUEST CURRENT UPDATE FIELDNAMES\n"
    #sock.sendall(message)

    # set fieldnames
    message = "S,SELECT UPDATE FIELDS,Most Recent Trade,Most Recent Trade Size,Total Volume,Most Recent Trade Time\n"
    sock.sendall(message)

    print "Connection set up."


    """ 
    message = "t%s\n" % "AMZN"

    sock.sendall(message)

    while True:

        data = sock.recv(4096)

        print data
    """


    # requesting all symbols
    print "Requesting symbols to watch......."
    numSym = 0

    # opening file with list of SYMs
    with open("syms.txt") as file:

        for line in file:

            # print all syms of file
            #print line.rstrip()

            # formatting symbol request
            req = "t%s\n" % line
            #print 'requesting %s' % line

            # sending request
            sock.send(req)

            numSym += 1

    print "Now watching {} syms.".format(numSym)

    #################################
    # redirecting watches to CLUSTER

    print "Redirecting feed......."

    data = ""

    while True:

        # receive data from IQFEED
        data = sock.recv(4096)

        # print to screen
        #print data

        # forwad data to CLUSTER
        clientsocket.send(data)