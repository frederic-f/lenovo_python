import sys
import socket
import subprocess
import pickle
from datetime import date


def read_data_socket_scanner (sock, recv_buffer=4096):
    """
    Read the informatio from the socket, in a buffered fashion, receiving only 4096 bytes at a time
    :param sock: the socket object
    :param recv_buffer: amount in bytes to receive per read
    :return: a string of received data
    """

    data = ""

    while True:
        buffer = sock.recv(recv_buffer)
        data += buffer

        # check if the end message string arrives
        if "!ENDMSG!" in buffer:
            break

    # remove the end message string
    data = data[:-8]

    return data


def read_data_socket_iqfeed (sock, nb_requests_sent=1, recv_buffer=4096):
    """
    Read the informatio from the socket, in a buffered fashion, receiving only 4096 bytes at a time
    :param sock: the socket object
    :param recv_buffer: amount in bytes to receive per read
    :return: a string of received data
    """

    data = ""
    nb_answers_recvd = 0 # to check that nb_answers_recvd matches nb_requests_sent

    while True:
        buffer = sock.recv(recv_buffer)
        data += buffer

        print("Reading buffer: {}...".format(buffer[:20]))

        # check if the end message string arrives
        if "!ENDMSG!" in buffer:
            nb_answers_recvd += 1

            if nb_answers_recvd == nb_requests_sent:
                break

    # Cleaning data
    # remove lines with !ENDMSG!
    data_lines = data.split('\n')
    data_clean = []

    for line in data_lines:
        if "!ENDMSG!" not in line:
            data_clean.append(line)

    data_to_return = '\n'.join(data_clean)

    return data_to_return


def send_requests(sock, requests):
    """Sends the requests one by one though the socket"""

    print("[*] Sending {NB_REQS} request through sock no {SOCK_NO}...".format(NB_REQS=len(requests),SOCK_NO=sock.fileno()))

    nb_requests_sent = 0

    for request in requests:
        sock.sendall(request)
        nb_requests_sent += 1

    print("[+] Requests sent")

    return nb_requests_sent



def make_iqfeed_req (reqs_list):


    print "\t[*] Making request to iqFeed..."

    # define (iqfeed client) server host, port and symbols to download
    host = "127.0.0.1"
    port = 9100 # historical data socket port

    # Open a streaming socket to the IQFeed server locally
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect((host, port))

    # set protocol to 6 to watch trades only
    message = "S,SET PROTOCOL,6.0\n"
    #sock.sendall(message)


    # Construct the message needed by IQFeed to retrieve data
    # 5-min data
    date = "20180919"
    sym = "AAPL"
    #message = "HIT,{SYM},300,{date} 075000,{date} 160000,,155500,160000,1,{SYM}\n".format(SYM=sym, date=date)
    sym = "AMZN"
    #message += "HIT,{SYM},300,{date} 075000,{date} 160000,,155500,160000,1,{SYM}\n".format(SYM=sym, date=date)
    # message = "HIX,{SYM},300,90\n".format(SYM=sym)


    # TODO function get_socks(socketCount=15) -> socks_list
    # create list of sockets

    socks = []
    socks_nb_requests = []

    for i in range(15):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        socks.append(sock)
        socks_nb_requests.append(0)

    print("Nombre de req a envoyer {}".format(len(reqs_list)))

    for i, req in enumerate(reqs_list):
        print("Rquete #{NUM}: {REQ}".format(NUM=i,REQ=req[:10]))
        
    # for each socket
    # assign requests to send
    # send requests
    mini_nb_reqs_per_socket = len(reqs) / 15
    nb_reqs_supplementaires = len(reqs) % 15
    for sock_index, sock in enumerate(socks):
        # with / we get the minimum number of request per socket
        # ex: 5 req, mini=0, max=1 ex: 17 reqs, mini=1, max=2
        # with # we get if index of said socket get an extra req
        # ex: 16 reqs, first socket will get an extra req (16%15=1)

        nb_reqs_to_send = mini_nb_reqs_per_socket
        if sock_index < nb_reqs_supplementaires:
            nb_reqs_to_send += 1

        #print("Socket # {I} has fileno {DESC}".format(I=i,DESC=sock.fileno()))
        #print("Socket # {I} gets {REQ_COUNT} req".format(I=sock_index,REQ_COUNT=nb_reqs_to_send))

        # calculating which reqs to send
        start_index = sock_index * mini_nb_reqs_per_socket
        if sock_index <= nb_reqs_supplementaires:
            start_index += sock_index
        else:
            start_index += nb_reqs_supplementaires

        end_index = start_index + nb_reqs_to_send
        #print("Socket # {SOCK_INDEX} sends [{START_INDEX}:{END_INDEX}]".
              #format(SOCK_INDEX=sock_index,START_INDEX=start_index,END_INDEX=end_index))

        nb_reqs_sent = send_requests(socks[sock_index], reqs_list[start_index:end_index])

        # TODO make sure the number of requests sents matahes number requests to be sent and answers recvd

        if nb_reqs_sent != nb_reqs_to_send:
            print("[-] Probem: Nb request sent != nb requests to send")

        socks_nb_requests[sock_index] = nb_reqs_sent


    # now receiving the answers
    for sock_index, sock in enumerate(socks):
        data = read_data_socket_iqfeed(sock, 2)

        print("[+] Sock #{SOCK_NUM} received".format(SOCK_NUM=sock.fileno()))
        print(data)


    sys.exit()

    num_reqs = 0

    for req in reqs_list:

        sock.sendall(req)

        print "req sent {}".format(req)

        num_reqs += 1

    print "[+] Requests sent"

    #print message
    #sock.sendall(message)

    """
    date = "20180919"
    sym = "AMZN"

    message = "HIT,{SYM},300,{date} 075000,{date} 160000,,155500,160000,1,{SYM}\n".format(SYM=sym, date=date)
    # message = "HIX,{SYM},300,90\n".format(SYM=sym)

    print message

    sock.sendall(message)
    """

    print "[*] Reading answers..."

    data = read_data_socket_iqfeed(sock, num_reqs)
    sock.close()

    print "[+] Answers read :"

    print data

    # Remove all the endlines and line-ending comma delimiter from each record
    #data = "".join(data.split('\r'))
    #data = data.replace(",\n", "\n")[:-1]

    # return data stream
    return data

if __name__ == "__main__":


    print "\n\n\n"
    print "\n-------------------------------------------------------------------------------"
    print "======== HIST GATEWAY ======== "
    print "-------------------------------------------------------------------------------"
    print "\n"

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
        print "\n[*] Waiting for connection on ({host},{port})...\n".format(host=host, port=port)

        # accept returns an open connection between server and client, along with address of client
        # connection
        (clientsocket, client_address) = serversocket.accept()

        try:
            #print >>sys.stderr, 'Connection from', client_address

            print "[+] Accepting connection from {}".format(client_address)

            req = read_data_socket_scanner(clientsocket)

            reqs = pickle.loads(req)

            print reqs

            data = make_iqfeed_req(reqs)

            data += "\n!ENDMSG!"

            print "\nAnswer to scanner\n"
            print data

            message = "This is an answer from iq_hist_gateway"
            message += "!ENDMSG!"

            clientsocket.sendall(data)

        finally:
            clientsocket.close()


        sys.exit()

    sys.exit()