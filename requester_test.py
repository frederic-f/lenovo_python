import threading

from requester import Requester


def run_requesters(requesters):
    for requester in requesters:
        try:
            threading.Thread(target=requester.request()).start()
        except Exception as e:
            print("[-] Thread could not be started: {}".format(str(e)))


requesters = []

request = "HIT,ANGI,300,20180919 075000,20180919 160000,,155500,160000,1,ANGI\n"    

for i in range(5):
    requester = Requester()
    requester.set_requests(request)
    requesters.append(requester)

run_requesters(requesters)