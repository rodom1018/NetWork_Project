# 20174744 Lee Dong Hyeon
from socket import *
from threading import Thread
import time, select
from os import sys
from sys import argv
send_message = None
did_print = 1

version = 0.2

def validnickname(nickname):
    if(len(nickname)>32):
        return False
    print(nickname)
    for letter in nickname:
        if((letter>='A') and (letter <='Z')):
            continue
        if((letter>='a') and (letter <='z')):
            continue     
        if(letter == '-'):
            continue
        return False
    return True
    
class Inputcheck(Exception):
    pass


serverName = "172.30.1.27"
serverPort = 24744
server_address = (serverName, serverPort)

for i in argv:
    print(i)

if len(sys.argv) <2 :
    print("please input nickname!")
    exit()

if len(sys.argv)>2:
    print("Space-included nickname is not allowed")
    exit()

nickname = sys.argv[1]

if(validnickname(nickname) == False):
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
welcomemessage= clientSocket.recv(1024)
print(welcomemessage.decode())
while True:

    try:
        
        clientSocket.send("dummy!".encode())
        sample=clientSocket.recv(1024)
        print(sample)


        """i, o, e = select.select([sys.stdin], [], [], 1)
        if i:
            send_message = sys.stdin.readline().rstrip("\n")
        else:
            raise Inputcheck"""

        send_message = input()

        if(send_message.startswith('/list')):
            send_message = send_message.replace("/list", "1")
        elif(send_message.startswith('/dm')):
            send_message = send_message.replace("/dm", "2")
        elif(send_message.startswith('/ex')):
            send_message = send_message.replace("/ex", "3")
        elif(send_message.startswith('/ver')):
            send_message = send_message.replace("/ver", "4")
        elif(send_message.startswith('/quit')):
            send_message = send_message.replace("/quit", "5")
            clientSocket.send(send_message.encode())
            print("bye bye ~")
            clientSocket.close()
            break
        elif(send_message.startswith('/rtt')):
            send_message = send_message.replace("/rtt", "6")

            send_time = time.time() * 1000.0
            clientSocket.send("dummy!".encode())
            sample=clientSocket.recv(1024)
            receive_time = time.time() * 1000.0

            print("Response time : {} ms".format(receive_time - send_time))
            print()
        elif(send_message.startswith('/')):
            print("wrong command ! try again")
            continue
        else:
            send_message ="0"+send_message

        # send to server
        print("this is client message!!!")
        print(send_message)
        clientSocket.send(send_message.encode())
        modifiedSentence = clientSocket.recv(1024)
        print(modifiedSentence.decode())

        if modifiedSentence.decode() == "":
            raise ConnectionResetError
        
        if modifiedSentence.decode() == "dummy!":
            continue

        if(send_message.startswith('4')):
            print(modifiedSentence.decode())
            print("and client version is {}".format(version))
        else:
            print("Reply From Server : ", modifiedSentence.decode())
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
        clientSocket.send("quit".encode())
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