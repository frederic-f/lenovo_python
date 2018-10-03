import sys
import socket

from tourniquet import Tourniquet


def read_data_scanner (sock, recv_buffer=4096):

    data = ""
    chunk = ""

    while "!ENDMSG!" not in chunk:
        # communication is in bytes -> so we decode
        chunk = sock.recv(4096).decode()
        data += chunk

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
    host = "localhost"
    port = 1235
    serversocket.bind((host, port))

    # become a server socket
    serversocket.listen(5)

    while (1):
        print("\n[*] Waiting for connection on ('{host}',{port})...".format(host=host, port=port))

        # connection with Scanner
        (clientsocket, client_address) = serversocket.accept()

        try:

            print("[+] Accepting connection from {}".format(client_address))

            print("\n[*] Receiving requests list")

            req = read_data_scanner(clientsocket)

            reqs = req.split("!SEP!")

            print("[+] List of requests received:\n")

            print(reqs)

            print("\n[*] Tournicotons\n")

            #########################

            tourniquet = Tourniquet(reqs)

            data = tourniquet.run()

            #########################

            # forward to scanner
            data += "\n!ENDMSG!"

            print("\nAnswer to scanner\n")
            print(data)

            clientsocket.sendall(data.encode())

        finally:
            clientsocket.close()


    sys.exit()