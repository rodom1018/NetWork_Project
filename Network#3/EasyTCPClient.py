# 20174744 Lee Dong Hyeon
from socket import *
from threading import Thread
import time, select
from os import sys

send_message = None
did_print = 1


def intro():
    print("<Menu>")
    print("1) convert text to UPPER-case")
    print("2) convert text to reverse order")
    print("3) get my IP address and  port number")
    print("4) get server running time")
    print("5) exit")
    print("Input Option ::", end=" ", flush=True)


class Inputcheck(Exception):
    pass


serverName = "172.30.1.19"
serverPort = 24744
server_address = (serverName, serverPort)

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_address)
except ConnectionRefusedError:
    # if server is off, and client connects to server.
    print("server didn't turned on! bye bye ~")
    clientSocket.close()
    exit()

while True:
    if did_print:
        intro()

    try:
        clientSocket.send("dummy!".encode())
        clientSocket.recv(1024)
        i, o, e = select.select([sys.stdin], [], [], 1)
        if i:
            send_message = sys.stdin.readline().rstrip("\n")
        else:
            did_print = 0
            raise Inputcheck

        if (int(send_message) > 5) or (int(send_message) < 1):
            # input is not correct number like 7
            print("wrong number ! Try Again! \n")
            did_print = 1
            continue
        elif send_message == "5":
            # when pressed 5
            clientSocket.send(send_message.encode())
            print("bye bye ~")
            clientSocket.close()
            break
        elif (send_message == "1") | (send_message == "2"):
            # when pressed 1,2
            message = input("Input sentence: ")
            send_message += message

        # send to server
        send_time = time.time() * 1000.0
        clientSocket.send(send_message.encode())
        modifiedSentence = clientSocket.recv(1024)
        receive_time = time.time() * 1000.0

        if modifiedSentence.decode() == "":
            raise ConnectionResetError

        print("Reply From Server : ", modifiedSentence.decode())
        print("Response time : {} ms".format(receive_time - send_time))
        did_print = 1
        print()
    except Inputcheck:
        continue
    except BrokenPipeError:
        # when executing client , server downed.
        print("server has suddenly terminated ! bye bye ~")
        clientSocket.close()
        break
    except ValueError:
        # input is not int like 'happy'
        print("you didn't type number ! Try Again ! \n ")
        did_print = 1
        continue
    except KeyboardInterrupt:
        # if pressed ctrl+c
        clientSocket.send(" ".encode())
        print("\n bye bye ~")
        clientSocket.close()
        break
    except ConnectionResetError:
        # when executing client , server downed.
        print("server has suddenly terminated ! bye bye ~")
        clientSocket.close()
        break
    except ConnectionAbortedError:
        # when executing client , server downed.
        print("server has suddenly terminated ! bye bye ~")
        clientSocket.close()
        break