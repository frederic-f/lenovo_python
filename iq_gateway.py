import sys
import socket
import subprocess
from datetime import date



def read_historical_data_socket (sock, recv_buffer=4096):
    """
    Read the informatio from the socket, in a buffered fashion, receiving only 4096 bytes at a time
    :param sock: the socket object
    :param recv_buffer: amount in bytes to receive per read
    :return: a string of received data
    """

    buffer = ""
    data = ""

    while True:
        data = sock.recv(recv_buffer)
        buffer += data

        # check if the end message string arrives
        if "!ENDMSG!" in buffer:
            break

    # remove the end message string
    # buffer = buffer[:-12]
    return buffer

def getDateOfLastTradingDay_YYYYMMDD():

    # date de la veille au format YYYYMMDD HHmmSS

    # ordinal form is timestamp like (1 is day 1 of year 1)

    # get ordinal date of today
    today_ordinal = date.today().toordinal()

    # how many days do we go back from today? We start with 1, yesterday
    offset = 1

    # if is it sunday or sat, we go back one more day
    while date.fromordinal(today_ordinal - offset).isoweekday() == 7 or date.fromordinal(today_ordinal - offset).isoweekday() == 6:
        offset += 1

    # get the ordinal form of the last trading day
    lastTradingDay = today_ordinal - offset

    # return string YYYYMMDD
    return date.fromordinal(lastTradingDay).strftime("%Y%m%d")


def make_iqfeed_req (sym):

    print "Downloading symbol: %s..." % sym

    # define (iqfeed client) server host, port and symbols to download
    host = "127.0.0.1"
    port = 9100 # historical data socket port

    # Open a streaming socket to the IQFeed server locally
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # set protocol to 6 to watch trades only
    message = "S,SET PROTOCOL,6.0\n"
    #sock.sendall(message)


    # Construct the message needed by IQFeed to retrieve data
    # 5-min data
    dateOfLastTradingDay = getDateOfLastTradingDay_YYYYMMDD()

    message = "HIT,{SYM},300,{date} 075000,{date} 160000,,093000,160000,1\n".format(SYM=sym, date=dateOfLastTradingDay)
    # message = "HIX,{SYM},300,90\n".format(SYM=sym)

    print message

    # Sending the historical data request message
    # and buffer the data
    sock.sendall(message)
    data = read_historical_data_socket(sock)
    sock.close()

    # Remove all the endlines and line-ending comma delimiter from each record
    data = "".join(data.split('\r'))
    data = data.replace(",\n", "\n")[:-1]

    # return data stream
    return data

if __name__ == "__main__":

    ######################################
    # start SERVER
    ######################################

    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host,
    # and a 1000+ port
    #host = socket.gethostname()
    host = "LENOVO"
    port = 1234
    serversocket.bind((host, port))

    # become a server socket
    serversocket.listen(5)

    while (1):
        print "\nWaiting for connection on {host} : {port}.......\n".format(host=host, port=port)

        # accept returns an open connection between server and client, along with address of client
        # connection
        (clientsocket, client_address) = serversocket.accept()

        try:
            #print >>sys.stderr, 'Connection from', client_address

            print "Accepting connection from {}".format(client_address)

            data = ""

            #receive the data
            while True:

                buffer = clientsocket.recv(4096)
                data += buffer

                # check if the end message string arrives
                if "!ENDMSG!" in buffer:
                    break

            # get rid of !ENDMSG!
            data = data[:-8]

            # receive the data -- OLD
            #data = clientsocket.recv(1024)

            # analysing request

            # first 4 chars are request type
            typeOfRequest = data[:4]

            #print "Request type: {}".format(typeOfRequest)

            ###################################################
            if typeOfRequest == "HIST":

                req = data.split(',')
                sym = req[1]

                #print >>sys.stderr "Request HIST for sym:  {}".format(sym)

                print "Request HIST for sym: {}".format(sym)

                # request data from iqfeed
                data = make_iqfeed_req(sym)

                print data

                # size of data to return to cluster
                MSGLEN = len(data)

                # forwarda data to cluster
                totalsent = 0
                while totalsent < MSGLEN:
                    sent = clientsocket.send(data[totalsent:])
                    if sent == 0:
                        raise RuntimeError(" socket connection broken")
                    totalsent = totalsent + sent

            ###############################################
            elif typeOfRequest == "SYMS":

                print "Request SYMS. Now receiving list of SYMs"

                # remove "SYMS," at beginning of message
                data = data[5:]

                syms = data.split(',')

                print "Writing list of SYMS to syms.txt"

                # writing all syms to file

                # erasing file
                handle = open("syms.txt", 'r+')
                handle.truncate(0)

                # Writing syms to file
                for sym in syms:

                    handle.write(sym + "\n")

                handle.close()

                print "Successfully written syms to syms.txt"

                # launching gateway for livefeed
                try:
                    retcode = subprocess.call("python" + " iqfeed_gtw_livefeed.py", shell=True)
                    
                    if retcode < 0:

                        print "Child was terminated by signal", -retcode

                        #print >> sys.stderr, "Child was terminated by signal", -retcode
                    else:

                        print "Child returned", retcode

                        #print >> sys.stderr, "Child returned", retcode

                except OSError as e:

                    print "execution failed", e

                    print >> sys.stderr, "Execution failed:", e

        finally:
            clientsocket.close()



    sys.exit()