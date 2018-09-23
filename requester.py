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

    def run(self):
        """Connects to the server, sends the reqs, read the answer"""

        print("[+] Requester {} running".format(self.sock.fileno()))

        print("[*] Request to send: {}".format(self.requests))

        req = "".join(self.requests)

        self.sock.sendall(req.encode())

        #for request in self.requests:
        #   self.sock.sendall(request)

        #data = self.read_data_socket_iqfeed()

        #print("Requester {NUM} received {DATA}".format(NUM=self.sock.fileno(),DATA=data))

        print("DATA SENT")

        #self.sock.close()

        return