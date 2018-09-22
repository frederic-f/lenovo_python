import socket


class Requester(object):
    """Manages everything related to a socket: sending, reading, cleaning data..."""

    def __init__(self, host="127.0.0.1", port=9100):
        """Initializes attributes"""

        self.host = host
        self.port = port
        self.sock = None
        self.requests = None
        self.nb_requests = 0

        # TODO make it over ssl
        # https://stackoverflow.com/questions/40440692/running-multiple-sockets-at-the-same-time-in-python

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def set_requests(self, requests):
        """Sets the requets to send to server"""
        self.requests = requests
        self.nb_requests = len(requests)

    def get_requests(self):

        return self.requests

    def read_data_socket_iqfeed(self,recv_buffer=4096):

        data = ""
        nb_answers_recvd = 0  # to check that nb_answers_recvd matches nb_requests_sent

        while True:
            buffer = self.sock.recv(recv_buffer)
            data += buffer

            print("Reading buffer: {}...".format(buffer[:20]))

            # check if the end message string arrives
            if "!ENDMSG!" in buffer:
                nb_answers_recvd += 1

                if nb_answers_recvd == self.nb_requests:
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

    def request(self):
        """Connects to the server, sends the reqs, read the answer"""

        print("[+] Requester {} running".format(self.sock.fileno()))

        print("[*] Request to send: {}".format(self.requests))

        req = "".join(self.requests)

        self.sock.sendall(req)

        #for request in self.requests:
        #   self.sock.sendall(request)

        #data = self.read_data_socket_iqfeed()

        #print("Requester {NUM} received {DATA}".format(NUM=self.sock.fileno(),DATA=data))

        print("DATA SENT")

        #self.sock.close()

        return