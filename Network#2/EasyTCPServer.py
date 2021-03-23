# 20174744 Lee Dong Hyeon
from socket import *
import time

# to measure how much time server is running.
start_time = time.time()

serverPort = 24744
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))
serverSocket.listen(1)
(connectionSocket, addr) = serverSocket.accept()
connectionSocket.settimeout(1)
print("The server is ready to receive on port 24744")

try:
    while True:
        try:
            sentence = connectionSocket.recv(1024).decode()
        except timeout:
            continue

        if sentence == "":
            # counter exception when ctrl+c or pressed 5
            connectionSocket.close()
            (connectionSocket, addr) = serverSocket.accept()

            sentence = connectionSocket.recv(1024).decode()

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
except KeyboardInterrupt:
    # when pressed ctrl+c on server
    serverSocket.close()
    connectionSocket.close()
    print("server down ! ")
    exit()