from socket import *
import threading

address = "nsl5.cau.ac.kr"
ports = [24744, 34744, 44744, 54744]
totalstate = 0
me = 5
serverPort = [0, 0]


def det_serverport(portnum):
    serverPort = [0, 0]
    temp_port = int(portnum)
    if temp_port == ports[0]:
        serverPort[0] = ports[3]
        serverPort[1] = ports[1]
        me = 0
    elif temp_port == ports[1]:
        serverPort[0] = ports[0]
        serverPort[1] = ports[2]
        me = 1
    elif temp_port == ports[2]:
        serverPort[0] = ports[1]
        serverPort[1] = ports[3]
        me = 2
    elif temp_port == ports[3]:
        serverPort[0] = ports[2]
        serverPort[1] = ports[0]
        me = 3


class Server(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    def run(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverPort = int(self.port)
        serverSocket.bind((address, serverPort))
        print("i'm ready to receive clients.")

        while True:
            (message, clientAddress) = serverSocket.recvfrom(2048)
            if message.decode() == "connect":
                serverSocket.sendto("connect!".encode, clientAddress)
                if clientAddress[1] == serverPort[0]:
                    totalstate += 10
                elif clientAddress[1] == serverPort[1]:
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
        state = 11
        timeout = 2
        Left_clientSocket = socket(AF_INET, SOCK_DGRAM)
        Left_clientSocket.settimeout(timeout)
        Right_clientSocket = socket(AF_INET, SOCK_DGRAM)
        Right_clientSocket.settimeout(timeout)
        serverPort = self.det_serverport()

        try:
            print("please wait. Try to Establish connection (left side)")
            Left_clientSocket.sendto("connect".encode(), (address, int(serverPort[0])))
            Left_clientSocket.recv(2048)
            print("Established connection! (left side)")
        except OSError as e:
            Left_clientSocket.close()
            state = state - 10
            print("Connection Establish fail.(left)")

        try:
            print("please wait. Try to Establish connection (right side)")
            Right_clientSocket.sendto("connect".encode(), (address, int(serverPort[1])))
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
            elif state == 11:
                send_message = input("input >>>")
                Left_clientSocket.sendto(
                    send_message.encode(), (address, int(serverPort[0]))
                )
                Left_clientSocket.recvfrom(2048)

                Right_clientSocket.sendto(
                    send_message.encode(), (address, int(serverPort[1]))
                )
                Right_clientSocket.recvfrom(2048)
            elif state == 10:
                send_message = input("input >>>")
                Left_clientSocket.sendto(
                    send_message.encode(), (address, int(serverPort[0]))
                )
                Left_clientSocket.recvfrom(2048)
            elif state == 1:
                Right_clientSocket.sendto(
                    send_message.encode(), (address, int(serverPort[1]))
                )
                Right_clientSocket.recvfrom(2048)


######################################
##########~!!start nain!!~############
######################################

port = input("input your port num!")
det_serverport(port)

server = Server(address, port)
server.start()

client = Client(address, port)
client.start()
