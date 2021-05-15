# 20174744 Lee Dong Hyeon
from socket import *
import time
import threading

version = 0.1
# if there exists connectionSocket, serverSocket
def TwoSocketClose(serverSocket, connectionSocket):
    serverSocket.close()
    connectionSocket.close()
    print("server closed!")


# if there only exist serverSocket
def OneSocketClose(ServerSocket):
    serverSocket.close()
    print("server closed!")


# thread function.
def handle_client(connectionSocket, addr):
    global number_of_client
    global totalnum_client
    number_of_client += 1
    totalnum_client += 1
    my_client_num = totalnum_client

    my_nick = client_nick[connectionSocket]
    while True:
        try:
            # when server abruptly downed, this is for closing thread - socket and thread itself.
            connectionSocket.settimeout(4)
            sentence = connectionSocket.recv(1024).decode()
        except:
            connectionSocket.close()
            exit()

        if sentence == "dummy!":
            connectionSocket.send("dummy!".encode())
            continue

        temp_sentence = sentence.lower()
        if sentence == "5" or "i hate professor" in temp_sentence:
            # counter exception when ctrl+c or pressed 5
            print(
                "<{}> left. There are <{}> users now ".format(
                    client_nick[connectionSocket], number_of_client - 1
                )
            )
            broadcast(
                "<{}> left. There are <{}> users now ".format(
                    client_nick[connectionSocket], number_of_client - 1
                ),
                connectionSocket,
            )
            socket_list.remove(connectionSocket)
            del client_addr[connectionSocket]
            del client_nick[connectionSocket]

            connectionSocket.close()
            number_of_client -= 1
            break

        if sentence[0] == "0":
            broadcast(sentence[1:], connectionSocket)
            connectionSocket.send("dummy!".encode())
        elif sentence[0] == "1":
            new_sentence = "List of clients info: \n"

            for client_socket in socket_list:
                new_sentence += "<nickname = {}, IP = {} , port = {}>\n".format(
                    client_nick[client_socket],
                    client_addr[client_socket][0],
                    client_addr[client_socket][1],
                )
            print(new_sentence)
            connectionSocket.send(new_sentence.encode())
        elif sentence[0] == "2":
            # dmcommand
            nickname = sentence.split(" ")[1]
            msg = sentence.split(sep=" ", maxsplit=2)[2]
            directmessage(msg, nickname)
            connectionSocket.send("dummy!".encode())
        elif sentence[0] == "3":
            # ex command
            nickname = sentence.split(" ")[1]
            msg = sentence.split(sep=" ", maxsplit=2)[2]
            exceptmessage(msg, my_nick, nickname)
            connectionSocket.send("dummy!".encode())
        elif sentence[0] == "4":
            # ver command
            connectionSocket.send("server version is {}".format(version).encode())
        elif sentence[0] == "6":
            # rtt command
            connectionSocket.send("dummy!".encode())
        else:
            print("invalid command")
            connectionSocket.send("dummy!".encode())


socket_list = []
client_addr = {}
client_nick = {}


def remove(connection):
    if connection in socket_list:
        socket_list.remove(connection)


def broadcast(message, me):
    for clients in socket_list:
        if clients != me:
            try:
                print(message)
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def directmessage(message, dmperson):
    for client in socket_list:
        if client_nick[client] == dmperson:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)


def exceptmessage(message, me, experson):
    for client in socket_list:
        if client_nick[client] != experson and client_nick[client] != me:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)


############################
### start! main funciton ###
############################
# to measure how much time server is running.
start_time = time.time()
alarm_time = 60

# number of clinents.
number_of_client = 0
totalnum_client = 0

# initial setting
serverPort = 24744
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.settimeout(0.5)

try:
    # when server downed even before first connection with client(no connectionsocket)
    serverSocket.bind(("nsl2.cau.ac.kr", serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on port 24744")
except KeyboardInterrupt:
    # pressed ctrl+c
    OneSocketClose(serverSocket)

flag = 1
nicknameflag = 1
try:
    while True:
        try:
            (connectionSocket, addr) = serverSocket.accept()
            nickname = connectionSocket.recv(1024).decode()
            if len(socket_list) < 8:
                for socket in socket_list:
                    if client_nick[socket] == nickname:
                        connectionSocket.send(
                            "that nickname is already used by another user. cannot connect".encode()
                        )
                        connectionSocket.close()
                        nicknameflag = 0
                if nicknameflag == 0:
                    nicknameflag = 1
                    continue
                temp_socket = connectionSocket
                socket_list.append(temp_socket)
                client_addr[temp_socket] = addr
                client_nick[temp_socket] = nickname

                connectionSocket.send(
                    "welcome <{}> to CAU network class chat room at <{}, {}>. You are <{}>th user".format(
                        nickname, "165.194.35.202", serverPort, totalnum_client + 1
                    ).encode()
                )
                print(
                    "<{}> joined. There are <{}> users connected.".format(
                        nickname, number_of_client + 1
                    )
                )
            else:
                connectionSocket.send("chatting room full. cannot connect".encode())
                connectionSocket.close()
                continue

        except timeout:
            continue

        flag = 0
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        thread.start()
except KeyboardInterrupt:
    # when pressed ctrl+c on server
    if flag == 1:
        OneSocketClose(serverSocket)
    else:
        TwoSocketClose(serverSocket, connectionSocket)
        for socket in socket_list:
            socket.close()
