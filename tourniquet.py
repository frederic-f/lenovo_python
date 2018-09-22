import select, threading

from requester import Requester


class Tourniquet(object):

    def __init__(self, reqs, nb_requesters=15):
        """Initiliazes the Tourniquester..."""

        # conditions de creation
        if not reqs:
            print("[-] At least one request must be passed to Tourniquet ")
            sys.exit()

        # setting the landscape
        self.reqs = reqs
        self.nb_requesters = nb_requesters

        print("[*] Creating {} requesters...".format(self.nb_requesters))
        self.requesters = self._create_requesters(self.nb_requesters)

        print("[+] {CREATED} requesters created (expecting {EXPECTED})\n".format(CREATED=len(self.requesters),EXPECTED=self.nb_requesters))

        print("[*] Assigning reqs to requesters...\n")

        self._list_reqs_assigned(self.requesters)

        self._assign_reqs_to_requesters(self.reqs, self.requesters)

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
            # with % we get if index of said socket get an extra req
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
        """Tells the requesters to send their requests ; then collects the data, cleans it and returns it"""

        socks = []

        # tells the requesters to send their requests
        # and grab their socks
        for requester in self.requesters:
            try:
                threading.Thread(target=requester.request()).start()
                socks.append(requester.sock)
            except Exception as e:
                print("[-] Thread could not be started: {}".format(str(e)))

        data = ""
        nb_of_answers = 0

        # collects the data from requesters
        # read from sockets that are available
        stay_in_loop = True
        while stay_in_loop:
            # this will block until at least one socket is ready
            ready_socks, _, _ = select.select(socks, [], [])
            for sock in ready_socks:
                buffer, addr = sock.recvfrom(1024)  # This is will not block
                print("received message: {}".format(buffer))

                # is there a complete answer?
                if "!ENDMSG" in buffer:
                    # count if all requests have been fullfilled
                    nb_of_answers += 1

                data += buffer

                print("{} answers received.".format(nb_of_answers))

                if nb_of_answers == len(self.reqs):
                    print("All reqs answered. Exiting loop")
                    stay_in_loop = False

            print("Looping again...\n")
        print("Exited from loop")
        print("[+] Data collected")
        #print data
        
        return self._process_data_to_return(data)

    def _process_data_to_return(self, data_to_process):

        print("[*] Cleaning data...")

        #print(data_to_process)

        data = ""

        for line in data_to_process.splitlines():
            if "!ENDMSG!" not in line:
                data += line + "\n"

        return data
