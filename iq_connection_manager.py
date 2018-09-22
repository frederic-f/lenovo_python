

import socket
import sys # for *args

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

def connectToHistPort():

    sym = "AMZN"

    print "Downloading symbol: %s..." % sym

    # Construct the message needed by IQFeed to retrieve data
    message = "HIT,%s,300,20180720 075000,,,155500,160000,1\n" % sym

    # define (iqfeed client) server host, port and symbols to download
    host = "127.0.0.1"
    port = 9100  # historical data socket port

    # Open a streaming socket to the IQFeed server locally
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Sending the historical data request message
    # and buffer the data
    sock.sendall(message)
    data = read_historical_data_socket(sock)
    sock.close()

    # Remove all the endlines and line-ending comma delimiter from each record
    data = "".join(data.split('\r'))
    data = data.replace(",\n", "\n")[:-1]

    # return data stream
    print data


def initializeFeed():

    pass


def connect():

    print "Initializing feed..."

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9300))

    message = "S,CONNECT\n"

    sock.sendall(message)
    
    while True:

        data = sock.recv(4096)

        print data

        # check if the end message string arrives
        if ",Connected," in data:
            break

    sock.close()


def disconnect():
    print
    "Initializing feed..."

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9300))

    message = "S,DISCONNECT\n"

    sock.sendall(message)

    while True:

        data = sock.recv(4096)

        print data

        # check if the end message string arrives
        if ",Not Connected," in data:
            break

    sock.close()
    

def stats():

    print "Getting stats..."


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9300))

    message = "S,REQUEST STATS\n"

    sock.sendall(message)
    answer = sock.recv(4096)

    sock.close()

    print answer


def reqCurrentFieldnames():

    print "Getting current Update Fieldnames..."


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9100))

    message = "S,REQUEST FUNDAMENTAL FIELDNAMES\n"

    sock.sendall(message)


    while True:

        data = sock.recv(4096)

        print data

        buffer += data

        # check if the end message string arrives
        if "!ENDMSG!" in buffer:
            break

        # check if the end message string arrives
        if "!SYNTAX_ERROR!" in buffer:
            break


    # remove the end message string
    # buffer = buffer[:-12]

    print buffer

    sock.close()



if __name__ == "__main__":

    options = { "connect" : connect,
                "disconnect" : disconnect,
                "stats" : stats,
                "fieldnames" : reqCurrentFieldnames}

    options[sys.argv[1]]()


    sys.exit()


    ###############################
    # open the feed
    # set protocol
    ###############################

    #print "connecting to hist port"

    #connectToHistPort()




