# 20174744 Lee Dong Hyeon
from socket import *
import time
import threading


def TwoSocketClose(serverSocket, connectionSocket):
    serverSocket.close()
    connectionSocket.close()
    print("server closed!")
    exit()


def OneSocketClose(ServerSocket):
    serverSocket.close()
    print("server closed!")
    exit()


def handle_client(connectionSocket, addr):
    global number_of_client
    global my_client_num

    number_of_client += 1
    my_client_num += 1

    print(
        f"Client {my_client_num} connected. Number of connected clients = {number_of_client} ."
    )

    while True:
        try:
            sentence = connectionSocket.recv(1024).decode()
        except timeout:
            continue

        if sentence == "":
            # counter exception when ctrl+c or pressed 5
            connectionSocket.close()
            number_of_client -= 1
            break

        if sentence[0] == "1":
            # when pressed 1
            sentence = sentence[1:]
            capitalizedSentence = sentence.upper()
            connectionSocket.send(capitalizedSentence.encode())
        elif sentence[0] == "2":
            # when pressed 2
            sentence = sentence[1:]
            ReverseSentence = "".join(reversed(sentence))
            connectionSocket.send(ReverseSentence.encode())
        elif sentence[0] == "3":
            # when pressed 3
            connectionSocket.send(
                (("client IP={} port={}".format(addr[0], addr[1])).encode())
            )
        elif sentence[0] == "4":
            # when pressed 4
            elapsed_time = (int)(time.time() - start_time)
            hour = (int)(elapsed_time / 3600)
            minute = (int)((elapsed_time % 3600) / 60)
            second = (int)((elapsed_time) % 60)
            time_sentence = " run time ={}:{}:{}".format(hour, minute, second)
            connectionSocket.send(time_sentence.encode())
    print(
        f"Client {my_client_num} disconnected. Number of connected clients = {number_of_client}"
    )


############################
### start! main funciton ###
############################
# to measure how much time server is running.
start_time = time.time()
alarm_time = 60

number_of_client = 0
my_client_num = 0

serverPort = 24744
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.settimeout(0.5)

try:
    # when server downed even before first connection with client(no connectionsocket)
    serverSocket.bind(("172.30.1.27", serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive on port 24744")
except KeyboardInterrupt:
    OneSocketClose(serverSocket)

flag = 1

try:
    while True:
        try:
            if time.time() - start_time >= alarm_time:
                print(f"[Alarm] Number of Client = {number_of_client}")
                alarm_time += 60

            (connectionSocket, addr) = serverSocket.accept()
        except timeout:
            continue

        flag = 0
        connectionSocket.settimeout(1)
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        thread.start()
except KeyboardInterrupt:
    # when pressed ctrl+c on server
    if flag == 0:
        TwoSocketClose(serverSocket, connectionSocket)
    else:
        OneSocketClose(serverSocket)
