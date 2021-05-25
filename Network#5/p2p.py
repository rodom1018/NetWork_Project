from socket import *
import threading

address = "nsl5.cau.ac.kr"
ports = [24744, 34744, 44744, 54744]
totalstate = 0
sequencenum = 0
me = 5
cache = [0, 0, 0, 0]
LeftRightPort = [0, 0]


def det_LeftRightPort(portnum):
    global me
    temp_port = int(portnum)
    if temp_port == ports[0]:
        LeftRightPort[0] = ports[3]
        LeftRightPort[1] = ports[1]
        me = 0
    elif temp_port == ports[1]:
        LeftRightPort[0] = ports[0]
        LeftRightPort[1] = ports[2]
        me = 1
    elif temp_port == ports[2]:
        LeftRightPort[0] = ports[1]
        LeftRightPort[1] = ports[3]
        me = 2
    elif temp_port == ports[3]:
        LeftRightPort[0] = ports[2]
        LeftRightPort[1] = ports[0]
        me = 3


class Server(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    def run(self):
        global totalstate
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverPort = int(self.port)
        serverSocket.bind((address, serverPort))

        while True:
            (message, clientAddress) = serverSocket.recvfrom(2048)

            welcome_message = message.decode()
            source_port = 0
            if welcome_message.startswith("connect"):
                welcome_message = welcome_message.replace("connect", "")
                source_port = int(welcome_message)
                serverSocket.sendto("connect!".encode(), clientAddress)
                if source_port == LeftRightPort[0]:
                    totalstate += 10
                elif source_port == LeftRightPort[1]:
                    totalstate += 1
            else:
                serverSocket.sendto("ACK!".encode(), clientAddress)
                new_message = message.decode()
                print(new_message[2:])
                node = int(new_message[0])
                nodeport = ports[node]
                seq = int(new_message[1])

                if seq == cache[node]:
                    print("detected duplicate message!")
                    continue
                cache[node] = seq

                tempstate = 0

                if nodeport == LeftRightPort[0]:
                    tempstate = totalstate - 10
                elif nodeport == LeftRightPort[1]:
                    tempstate = totalstate - 1

                if tempstate == 10:
                    serverSocket.sendto(message, (address, int(LeftRightPort[0])))
                    serverSocket.recvfrom(2048)
                elif tempstate == 1:
                    serverSocket.sendto(
                        new_message.encode(), (address, int(LeftRightPort[1]))
                    )
                    serverSocket.recvfrom(2048)


class Client(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    def run(self):
        global totalstate, sequencenum, me
        state = 11
        timeout = 2
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(timeout)

        message = "connect" + self.port
        try:
            print("please wait. Try to Establish connection (left side)")
            clientSocket.sendto(message.encode(), (address, LeftRightPort[0]))
            clientSocket.recv(2048)
            print("Established connection! (left side)")
        except OSError as e:
            state = state - 10
            print("Connection Establish fail.(left)")

        try:
            print("please wait. Try to Establish connection (right side)")
            clientSocket.sendto(message.encode(), (address, LeftRightPort[1]))
            clientSocket.recv(2048)
            print("Established connection!(right side)")
        except OSError as e:
            state = state - 1
            print("Connection Establish fail. (right)")

        clientSocket.settimeout(None)
        totalstate += state
        ##state = 11: left, right both connected, 10= left connected , 01 = right connected , 00 = both not connected.
        while True:

            send_message = input("input >>>")
            sequencenum += 1
            send_message = str(me) + str(sequencenum % 10) + send_message
            if totalstate == 11:
                clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[0]))
                )

                clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[1]))
                )
                clientSocket.recvfrom(2048)
                clientSocket.recvfrom(2048)
            elif totalstate == 10:
                clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[0]))
                )
                clientSocket.recvfrom(2048)
            elif totalstate == 1:
                clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[1]))
                )
                clientSocket.recvfrom(2048)


######################################
##########~!!start nain!!~############
######################################

port = input("input your port num!")
det_LeftRightPort(int(port))

server = Server(address, port)
server.start()

client = Client(address, port)
client.start()
