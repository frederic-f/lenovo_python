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
    buffer = buffer[:-12]
    return buffer


if __name__ == "__main__":

    # define server host, port and symbols to download
    host = "127.0.0.1"
    port = 9100 # historical data socket port
    syms = ["SPY", "AAPL"]

    # download each symbol to disk
    for sym in syms:

        print "Downloading symbol: %s..." % sym

        # Construct the message needed by IQFeed to retrieve data
        message = "HIT,%s,60,20180709 075000,,,093000,160000,1\n" % sym

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
        data = data.replace(",\n","\n")[:-1]

        # Print data stream
        print data

        # Write the data stream to disk