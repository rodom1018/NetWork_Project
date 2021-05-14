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
    print(
        "Client {} connected. Number of connected clients = {}".format(
            my_client_num, number_of_client
        )
    )
    while True:
        try:
            # when server abruptly downed, this is for closing thread - socket and thread itself.
            """ 이 문장 나중에 원상복구 해야함 .!!!! 
            connectionSocket.settimeout(3)"""

            sentence = connectionSocket.recv(1024).decode()
        except:
            connectionSocket.close()
            exit()

        if sentence == " " or sentence == "5" or sentence =="quit":
            # counter exception when ctrl+c or pressed 5
            print("<nickname left. There are N users now ")
            connectionSocket.close()
            number_of_client -= 1
            break

        if sentence == "dummy!":
            connectionSocket.send("dummy!".encode())
            continue
        
        if sentence[0] == "0" :
            broadcast(sentence[1:], connectionSocket)
            connectionSocket.send("dummy!".encode())
        elif sentence[0] == "1":
            new_sentence = "List of clients info: \n"
            
            for client_socket in socket_list:
                #new_sentence+="<nickname = {}, IP = {} , port = {}>".format(client_nick[client_socket], client_addr[client_socket][0], client_addr[client_socket][1])
                new_sentence+="<nickname = {}>\n".format(client_nick[client_socket])
            print("this is new sentence")
            print(new_sentence)
            connectionSocket.send(new_sentence.encode())
        elif sentence[0] == "2":
            #dmcommand
            nickname = sentence.split(' ')[1]
            msg = sentence.split(sep=' ', maxsplit=2)[2]
            directmessage(msg, nickname)
        elif sentence[0] == "3":
            # ex command
            nickname = sentence.split(' ')[1]
            msg = sentence.split(sep=' ', maxsplit=2)[2]
            exceptmessage(msg, nickname)
        elif sentence[0] == "4":
            # ver command
            connectionSocket.send("server version is {} , ".format(version).encode())
        elif sentence[0] == "6":
            # rtt command
            sample=connectionSocket.recv(1024)
            connectionSocket.send("dummy!".encode())

    print(
        "Client {} disconnected. Number of connected clients = {}".format(
            my_client_num, number_of_client
        )
    )

socket_list = []
client_addr={}
client_nick={}

def remove(connection):
    if connection in socket_list:
        socket_list.remove(connection)

def broadcast(message, me):
    for clients in socket_list:
        if clients!=me:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def selfmessage(message, me):
    for clients in socket_list:
        if clients==me:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def directmessage(message, dmperson):
    for clients in socket_list:
        if clients==dmperson:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def exceptmessage(message, me ,experson):
    for clients in socket_list:
        if clients != experson and clients != me:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


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
serverIP="172.30.1.27"
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.settimeout(0.5)

try:
    # when server downed even before first connection with client(no connectionsocket)
    serverSocket.bind(("172.30.1.27", serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on port 24744")
except KeyboardInterrupt:
    # pressed ctrl+c
    OneSocketClose(serverSocket)

flag = 1

try:
    while True:
        try:
            # every 60 seconds, it alrams.
            if time.time() - start_time >= alarm_time:
                print("[Alarm] Number of Client = {}".format(number_of_client))
                alarm_time += 60

            (connectionSocket, addr) = serverSocket.accept()
            nickname = connectionSocket.recv(1024).decode()
            connectionSocket.send("welcome <{}> to CAU network class room at <{}, {}>. You are <{}>th user".format(nickname, serverIP, serverPort, totalnum_client).encode())
            print("<{}> joined. There are <{}> user.".format(nickname, number_of_client))
            temp_socket = connectionSocket
            if(len(socket_list) <8):
                socket_list.append(temp_socket)
                client_addr[temp_socket] = addr
                client_nick[temp_socket] = nickname
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
