import threading
import select

from requester import Requester


def run_requesters(requesters):

    socks = []

    for requester in requesters:
        try:
            threading.Thread(target=requester.request()).start()

            socks.append(requester.sock)

        except Exception as e:
            print("[-] Thread could not be started: {}".format(str(e)))


    # read from sockets that are available
    while True:
        # this will block until at least one socket is ready
        ready_socks, _, _ = select.select(socks, [], [])
        for sock in ready_socks:
            data, addr = sock.recvfrom(1024)  # This is will not block
            print "received message:", data

        print("Out of the looop")


requesters = []

requests = []

requests.append("HIT,ANGI,300,20180919 075000,20180919 160000,,155500,160000,1,ANGI\n")
requests.append("HIT,ANGO,300,20180919 075000,20180919 160000,,155500,160000,1,ANGO\n")
requests.append("HIT,AMD,300,20180919 075000,20180919 160000,,155500,160000,1,AMD\n")
requests.append("HIT,AQN,300,20180919 075000,20180919 160000,,155500,160000,1,AQN\n")
requests.append("HIT,AATH,300,20180919 075000,20180919 160000,,155500,160000,1,AATH\n")
requests.append("HIT,AAPL,300,20180919 075000,20180919 160000,,155500,160000,1,AAPL\n")


for i in range(2):
    requester = Requester()
    requester.set_requests(requests)
    requesters.append(requester)

run_requesters(requesters)