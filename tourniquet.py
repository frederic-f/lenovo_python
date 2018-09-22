from requester import Requester


class Tourniquet(object):

    def __init__(self, reqs):
        """Initiliazes the Tourniquester..."""

        # setting the landscape
        self.reqs_from_client = reqs
        self.nb_requesters = 10

        print("[*] Creating {} requesters...".format(self.nb_requesters))
        self.requesters = self._create_requesters(self.nb_requesters)

        print("[+] {CREATED} requesters created (expecting {EXPECTED})\n".format(CREATED=len(self.requesters),EXPECTED=self.nb_requesters))

        print("[*] Assigning reqs to requesters...\n")

        self._list_reqs_assigned(self.requesters)

        self._assign_reqs_to_requesters(self.reqs_from_client, self.requesters)

        self._list_reqs_assigned(self.requesters)

        print("\n[+] Reqs assigned\n")

        print("[+] Exiting __init__ tourniquet\n")

        return

    def _create_requesters(self, nb_of_requesters):
        requesters = []
        for i in range(nb_of_requesters):
            requester = Requester()
            requesters.append(requester)
        return requesters

    def _list_reqs_assigned(self, requesters):
        """Lists the reqs assigned to each requester"""
        for requester in requesters:
            print(requester.get_requests())
        return

    def _assign_reqs_to_requesters(self, reqs, requesters):
        """Assigs the reqs equally between the Requesters"""

        # debug
        for i, req in enumerate(reqs):
            print("Req #{NUM}: {REQ}".format(NUM=i, REQ=req[:10]))
            
        # for each socket
        # assign requests to send
        # send requests
        mini_nb_reqs_per_socket = len(reqs) / len(requesters)
        nb_reqs_supplementaires = len(reqs) % len(requesters)

        for requester_index, requester in enumerate(requesters):
            # with / we get the minimum number of request per socket
            # ex: 5 req, mini=0, max=1 ex: 17 reqs, mini=1, max=2
            # with # we get if index of said socket get an extra req
            # ex: 16 reqs, first socket will get an extra req (16%15=1)

            nb_reqs_to_send = mini_nb_reqs_per_socket
            if requester_index < nb_reqs_supplementaires:
                nb_reqs_to_send += 1

            # calculating which reqs to send
            start_index = requester_index * mini_nb_reqs_per_socket
            if requester_index <= nb_reqs_supplementaires:
                start_index += requester_index
            else:
                start_index += nb_reqs_supplementaires

            end_index = start_index + nb_reqs_to_send

            # give requester the reqs to execute
            requester.set_requests(reqs[start_index:end_index])

            # TODO make sure the number of requests sents matahes number requests to be sent and answers recvd

        return

    def run(self):
        """Tells the requesters to send their requests, collects, cleans and returns the data"""
