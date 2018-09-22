import sys
import socket

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


def make_iqfeed_req (sym):

    print "Downloading symbol: %s..." % sym

    # Construct the message needed by IQFeed to retrieve data
    message = "HIT,%s,300,20180720 075000,,,155500,160000,1\n" % sym

    # define (iqfeed client) server host, port and symbols to download
    host = "127.0.0.1"
    port = 9300 # historical data socket port

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
    return data


if __name__ == "__main__":

    print "creating socket"

    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host,
    # and a 1000+ port
    host = "127.0.0.1"
    port = 1234
    serversocket.bind((host, port))
    # become a server socket


    serversocket.listen(5)

    while (1):
        print "Waiting for connection on", host, ":", port

        # accept returns an open connection between server and client, along with address of client
        # connection
        (clientsocket, client_address) = serversocket.accept()

        try:
            print >>sys.stderr, 'Connection from', client_address

            # receive the data (SYM)
            sym = clientsocket.recv(1024)
            print >>sys.stderr, 'Request data for: SYM "%s"' % sym

            # request data from iqfeed
            data = make_iqfeed_req(sym)

            # size of data to return to cluster
            MSGLEN = len(data)

            # forwarda data to cluster
            totalsent = 0
            while totalsent < MSGLEN:
                sent = clientsocket.send(data[totalsent:])
                if sent == 0:
                    raise RuntimeError(" socket connection broken")
                totalsent = totalsent + sent



        finally:
            clientsocket.close()


