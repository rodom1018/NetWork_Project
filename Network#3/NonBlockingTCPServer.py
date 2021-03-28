# 20174744 Lee Dong Hyeon
from socket import *
import time
import select

# converting message, or make message (message for client)
def convertmessage(write_socket, sentence):
    if sentence[0] == "1":
        # when pressed 1
        sentence = sentence[1:]
        capitalizedSentence = sentence.upper()
        return capitalizedSentence
    elif sentence[0] == "2":
        # when pressed 2
        sentence = sentence[1:]
        ReverseSentence = "".join(reversed(sentence))
        return ReverseSentence
    elif sentence[0] == "3":
        # when pressed 3
        return "client IP={} port={}".format(
            addresses[write_socket][0], addresses[write_socket][1]
        )

    elif sentence[0] == "4":
        # when pressed 4
        elapsed_time = (int)(time.time() - start_time)
        hour = (int)(elapsed_time / 3600)
        minute = (int)((elapsed_time % 3600) / 60)
        second = (int)((elapsed_time) % 60)
        time_sentence = " run time ={}:{}:{}".format(hour, minute, second)
        return time_sentence


##################################
########start main! ##############
##################################

start_time = time.time()
alarm_time = 60
serverPort = 24744

number_of_client = 0
my_client_num = 0

# initial settings
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("nsl2.cau.ac.kr", serverPort))
serverSocket.listen(1)
print("The server is ready to receive on port 24744")
temporary_socket = socket(AF_INET, SOCK_STREAM)
read_socket_list = [
    serverSocket,
]
write_socket_list = []
messages = {}
addresses = {}

try:
    while True:
        # alarm every 60 seconds
        if time.time() - start_time > alarm_time:
            print("[Alarm] Number of Client = {}".format(number_of_client))
            alarm_time += 60
        try:
            # if there is any terminated socket, remove from the list. (not to read terminated socket)
            read_socket_list.remove(temporary_socket)
            del addresses[temporary_socket]
        except:
            pass

        # select function
        conn_read_socket, conn_write_socket, conn_except_socket = select.select(
            read_socket_list, write_socket_list, [], 0.5
        )

        # reading section(detect any changes)
        for conn_socket in conn_read_socket:
            if conn_socket == serverSocket:
                (connectionSocket, addr) = serverSocket.accept()
                addresses[connectionSocket] = addr

                number_of_client += 1
                my_client_num += 1
                print(
                    "Client {} connected. Number of connected clients = {}.".format(
                        my_client_num, number_of_client
                    )
                )
                connectionSocket.setblocking(0)
                read_socket_list.append(connectionSocket)

            else:
                sentence = conn_socket.recv(1024).decode()
                if sentence == " " or sentence == "5":
                    number_of_client -= 1
                    print(
                        "Client {} disconnected. Number of connected clients = {}".format(
                            my_client_num, number_of_client
                        )
                    )
                    temporary_socket = conn_socket
                    break
                messages[conn_socket] = sentence
                if conn_socket not in write_socket_list:
                    write_socket_list.append(conn_socket)

        # writing section(detect any changes)
        for write_socket in conn_write_socket:
            # convert message and send to client
            sentence = messages.get(write_socket)
            new_sentence = convertmessage(write_socket, sentence)
            write_socket.send(new_sentence.encode())

            # delete sended message
            del messages[write_socket]
            write_socket_list.remove(write_socket)

except KeyboardInterrupt:
    # ctrl+c on server program
    serverSocket.close()
    temporary_socket.close()

    # deal with situation when conn_socket doesn't exist.
    try:
        conn_socket.close()
    except:
        pass

    print("server closed!")
    exit()