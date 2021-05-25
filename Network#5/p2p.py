from socket import *
import threading

address = "nsl5.cau.ac.kr"
ports = [24744, 34744, 44744, 54744]
totalstate = 0
sequencenum = 0
LeftRightPort = [0, 0]


def det_LeftRightPort(portnum):
    temp_port = int(portnum)
    if temp_port == ports[0]:
        LeftRightPort[0] = ports[3]
        LeftRightPort[1] = ports[1]
    elif temp_port == ports[1]:
        LeftRightPort[0] = ports[0]
        LeftRightPort[1] = ports[2]
    elif temp_port == ports[2]:
        LeftRightPort[0] = ports[1]
        LeftRightPort[1] = ports[3]
    elif temp_port == ports[3]:
        LeftRightPort[0] = ports[2]
        LeftRightPort[1] = ports[0]


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
        print("i'm ready to receive clients.")

        while True:
            (message, clientAddress) = serverSocket.recvfrom(2048)
            welcome_message = message.decode()
            source_port = 0
            if welcome_message.startswith("connect"):
                serverSocket.sendto("connect!".encode(), clientAddress)
                welcome_message = welcome_message.replace("connect", "")
                source_port = int(welcome_message)
                if source_port == LeftRightPort[0]:
                    totalstate += 10
                elif source_port == LeftRightPort[1]:
                    totalstate += 1
            else:
                print(message.decode())
                serverSocket.sendto("Listened".encode(), clientAddress)


class Client(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    def run(self):
        global totalstate
        state = 11
        timeout = 2
        Left_clientSocket = socket(AF_INET, SOCK_DGRAM)
        Left_clientSocket.settimeout(timeout)
        Right_clientSocket = socket(AF_INET, SOCK_DGRAM)
        Right_clientSocket.settimeout(timeout)

        message = "connect" + self.port
        try:
            print("please wait. Try to Establish connection (left side)")
            Left_clientSocket.sendto(message.encode(), (address, LeftRightPort[0]))
            Left_clientSocket.recv(2048)
            print("Established connection! (left side)")
        except OSError as e:
            Left_clientSocket.close()
            state = state - 10
            print("Connection Establish fail.(left)")

        try:
            print("please wait. Try to Establish connection (right side)")
            Right_clientSocket.sendto(message.encode(), (address, LeftRightPort[1]))
            Right_clientSocket.recv(2048)
            print("Established connection!(right side)")
        except OSError as e:
            Right_clientSocket.close()
            state = state - 1
            print("Connection Establish fail. (right)")
        totalstate += state
        ##state = 11: left, right both connected, 10= left connected , 01 = right connected , 00 = both not connected.
        while True:
            if state == 0:
                break

            send_message = input("input >>>")
            sequencenum += 1

            if state == 11:
                Left_clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[0]))
                )
                Left_clientSocket.recvfrom(2048)

                Right_clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[1]))
                )
                Right_clientSocket.recvfrom(2048)
            elif state == 10:
                Left_clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[0]))
                )
                Left_clientSocket.recvfrom(2048)
            elif state == 1:
                Right_clientSocket.sendto(
                    send_message.encode(), (address, int(LeftRightPort[1]))
                )
                Right_clientSocket.recvfrom(2048)


######################################
##########~!!start nain!!~############
######################################

port = input("input your port num!")
det_LeftRightPort(int(port))

server = Server(address, port)
server.start()

client = Client(address, port)
client.start()
