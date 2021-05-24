from socket import *
import threading


class Server(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    def run(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverPort = int(self.port)
        serverSocket.bind(("nsl5.cau.ac.kr", serverPort))
        print("i'm ready to receive clients.")

        while True:
            (message, clientAddress) = serverSocket.recvfrom(2048)
            sentence = message.decode()
            print(sentence)
            serverSocket.sendto("I listened you!!".encode(), clientAddress)


class Client(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    def run(self):
        serverName = "nsl5.cau.ac.kr"
        serverPort = 0
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        while True:
            send_message = input("input >>>")
            if self.port == "24744":
                serverPort = 34744
            if self.port == "34744":
                serverPort = 24744
            print(serverPort)
            print(type(serverPort))
            clientSocket.sendto(send_message.encode(), (serverName, serverPort))
            (modifiedSentence, serverAddress) = clientSocket.recvfrom(2048)
            print(modifiedSentence.decode())


address = "nsl5.cau.ac.kr"
port = input("input your port num!")

server = Server(address, port)
server.start()

client = Client(address, port)
client.start()
