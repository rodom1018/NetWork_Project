# 20174744 Lee Dong Hyeon
from socket import *
from threading import Thread
import time, select
from os import sys
from sys import argv

send_message = None
version = 0.2


def validnickname(nickname):
    if len(nickname) > 32:
        return False
    for letter in nickname:
        if (letter >= "A") and (letter <= "Z"):
            continue
        if (letter >= "a") and (letter <= "z"):
            continue
        if letter == "-":
            continue
        return False
    return True


class Inputcheck(Exception):
    pass


serverName = "nsl2.cau.ac.kr"
serverPort = 24744
server_address = (serverName, serverPort)
# to catch less / more sys.argv
# like python Client.py(no nickname)
if len(sys.argv) < 2:
    print("please input nickname!")
    exit()

if len(sys.argv) > 2:
    print("Space-included nickname is not allowed")
    exit()

nickname = sys.argv[1]

# check whether nickname is valid.
if validnickname(nickname) == False:
    print("invalid format of nickname")
    exit()


try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_address)
except ConnectionRefusedError:
    # if server is off, and client connects to server.
    print("server didn't turned on! bye bye ~")
    clientSocket.close()
    exit()

clientSocket.send(nickname.encode())
welcomemessage = clientSocket.recv(1024).decode()
if (
    welcomemessage == "chatting room full. cannot connect"
    or welcomemessage == "that nickname is already used by another user. cannot connect"
):
    print(welcomemessage)
    clientSocket.close()
    exit()

print(welcomemessage)

while True:

    try:

        clientSocket.send("dummy!".encode())
        sample = clientSocket.recv(1024).decode()
        if sample != "dummy!":
            sample = sample.replace("dummy!", "")
            print(sample)
            print()
        i, o, e = select.select([sys.stdin], [], [], 1)
        if i:
            send_message = sys.stdin.readline().rstrip("\n")
        else:
            raise Inputcheck

        # encode into some binary data(plain -> binary data)
        if send_message.startswith("\list"):
            send_message = send_message.replace("\list", "1")
        elif send_message.startswith("\dm"):
            send_message = send_message.replace("\dm", "2")
        elif send_message.startswith("\ex"):
            send_message = send_message.replace("\ex", "3")
        elif send_message.startswith("\\ver"):
            send_message = send_message.replace("\\ver", "4")
        elif send_message.startswith("\quit"):
            send_message = send_message.replace("\quit", "5")
            clientSocket.send(send_message.encode())
            print("gg~")
            clientSocket.close()
            break
        elif send_message.startswith("\\rtt"):
            # \rtt
            send_message = send_message.replace("\\rtt", "6")

            send_time = time.time() * 1000.0
            clientSocket.send("dummy!".encode())
            sample = clientSocket.recv(1024)
            receive_time = time.time() * 1000.0

            print("Response time : {} ms".format(receive_time - send_time))
            print()
        elif send_message.startswith("\date"):
            send_message = send_message.replace("\date", "7")
        elif send_message.startswith("\\"):
            print("invalid commnad")
            continue
        else:
            send_message = "0" + send_message

        # send to server
        clientSocket.send(send_message.encode())
        modifiedSentence = clientSocket.recv(1024)

        if modifiedSentence.decode() == "you hate professor?":
            # catched by server "i hate professor"
            print(modifiedSentence.decode() + "gg ~ ")
            clientSocket.close()
            exit()

        if modifiedSentence.decode() == "dummy!":
            continue

        if send_message.startswith("4"):
            # /ver
            print(
                modifiedSentence.decode().replace("dummy", " ")
                + "    client version is {}".format(version)
            )
            print()
        else:
            print(modifiedSentence.decode())
            print()
    except Inputcheck:
        continue
    except BrokenPipeError:
        # when executing client , server downed.
        print("server has suddenly terminated ! bye bye ~")
        clientSocket.close()
        break
    except KeyboardInterrupt:
        # if pressed ctrl+c
        clientSocket.send("5".encode())
        print("\n gg~")
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
