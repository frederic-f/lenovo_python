import sys
import socket
import pickle

from tourniquet import Tourniquet


def read_data_socket_scanner (sock, recv_buffer=4096):
    """
    Read the informatio from the socket, in a buffered fashion, receiving only 4096 bytes at a time
    :param sock: the socket object
    :param recv_buffer: amount in bytes to receive per read
    :return: a string of received data
    """

    data = ""
    chunks = []

    while True:
        # communication is in bytes -> so we decode
        chunk = sock.recv(4096).decode()
        data += chunk

        # check if the end message string arrives
        if "!ENDMSG!" in chunk:
            break

    # remove the end message string
    data = data[:-8]

    print(data)

    return data


if __name__ == "__main__":

    print("\n\n-------------------------------------------------------------------------------")
    print("======== HIST GATEWAY V 0.2 ======== ")
    print("-------------------------------------------------------------------------------")
    print("\n")

    ######################################
    # start SERVER
    ######################################

    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host = socket.gethostname()
    host = "LENOVO"
    port = 1235
    serversocket.bind((host, port))

    # become a server socket
    serversocket.listen(5)

    while (1):
        print("\n[*] Waiting for connection on ('{host}',{port})...".format(host=host, port=port))

        # accept returns an open connection between server and client, along with address of client
        # connection
        (clientsocket, client_address) = serversocket.accept()

        try:

            print("[+] Accepting connection from {}".format(client_address))

            print("\n[*] Receiving requests list")

            req = read_data_socket_scanner(clientsocket)

            #reqs = pickle.loads(req)
            reqs = req.split("!SEP!")

            print("[+] List of requests received\n")

            print(reqs)

            print("\n[*] Tournicotons\n")

            #########################

            tourniquet = Tourniquet(reqs)

            data = tourniquet.run()

            #########################

             #data = make_iqfeed_req(reqs)

            data += "\n!ENDMSG!"

            print("\nAnswer to scanner\n")
            print(data)

            clientsocket.sendall(data.encode())

        finally:
            clientsocket.close()

    sys.exit()