# 20174744 Lee Dong Hyeon
from socket import *
import time


def intro():
    print("<Menu>")
    print("1) convert text to UPPER-case")
    print("2) convert text to reverse order")
    print("3) get my IP address and  port number")
    print("4) get server running time")
    print("5) exit")


serverName = "127.30.1.27"
serverPort = 34744


clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind((serverName, 0))

# wait reply 5 seconds from server, if message does not come, client thinks server has downed.
clientSocket.settimeout(5)

while True:

    intro()

    try:
        send_message = input("Input option: ")
        experiement_num = (int)(send_message)
    except KeyboardInterrupt:
        # when pressed ctrl+c
        clientSocket.sendto(" ".encode(), (serverName, serverPort))
        print("\n bye bye ~")
        clientSocket.close()
        break
    except:
        # when you didn't type number like 'apple'
        print("you didn't type number ! Try Again ! \n ")
        clientSocket.sendto(" ".encode(), (serverName, serverPort))
        continue

    if (int(send_message) > 5) or (int(send_message) < 1):
        # if you didn't type correct number
        print("wrong number ! Try Again! \n")
        clientSocket.sendto(" ".encode(), (serverName, serverPort))
        continue
    elif send_message == "5":
        # pressed 5
        clientSocket.sendto(send_message.encode(), (serverName, serverPort))
        print("bye bye ~")
        break
    elif (send_message == "1") | (send_message == "2"):
        # pressed 1, 2
        message = input("Input sentence: ")
        send_message += message

    # send message to server
    send_time = time.time() * 1000.0
    clientSocket.sendto(send_message.encode(), (serverName, serverPort))

    try:
        # wait reply 5 seconds from server, if message does not come, client thinks server has downed.
        (modifiedSentence, serverAddress) = clientSocket.recvfrom(2048)
        receive_time = time.time() * 1000.0
        print("Reply From Server : ", modifiedSentence.decode())
        print("Response time : {} ms".format(receive_time - send_time))
        print()
    except timeout:
        print("sever has downed ! bye bye ~")
        break
    except ConnectionResetError:
        print("sever has downed ! bye bye ~")
        break
