# 20174744 Lee Dong Hyeon
from socket import *
import time

start_time = time.time()
serverPort = 34744
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("The server is ready to receive on port 34744")

# to react to ctrl+c , serverSocket.recvfrom waits forever .
serverSocket.settimeout(1)

try:
    while True:
        try:
            # to react to ctrl+c , serverSocket.recvfrom waits forever .
            (message, clientAddress) = serverSocket.recvfrom(2048)
        except timeout:
            continue

        sentence = message.decode()

        if sentence[0] == "1":
            # pressed 1
            sentence = sentence[1:]
            capitalizedSentence = sentence.upper()
            serverSocket.sendto(capitalizedSentence.encode(), clientAddress)
        elif sentence[0] == "2":
            # pressed 2
            sentence = sentence[1:]
            ReverseSentence = "".join(reversed(sentence))
            serverSocket.sendto(ReverseSentence.encode(), clientAddress)
        elif sentence[0] == "3":
            # pressed 3
            serverSocket.sendto(
                (
                    "client IP={} port={}".format(clientAddress[0], clientAddress[1])
                ).encode(),
                clientAddress,
            )
        elif sentence[0] == "4":
            # pressed 4
            elapsed_time = (int)(time.time() - start_time)
            hour = (int)(elapsed_time / 3600)
            minute = (int)((elapsed_time % 3600) / 60)
            second = (int)((elapsed_time) % 60)
            time_sentence = " run time = {}:{}:{}".format(hour, minute, second)
            serverSocket.sendto(time_sentence.encode(), clientAddress)
except KeyboardInterrupt:
    # reacting to ctrl+c
    print("server down! ")
    exit()