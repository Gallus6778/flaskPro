#!/usr/bin/env python
# coding: utf-8

# In[1]:

import socket, threading
from chatbot_module import Pas_internet as pi
# In[ ]:


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        
    def run(self):
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode("utf8")
            if msg=='bye':
                self.csocket.send(message_emis)
                break

            print ("from client", msg)
            reponse = list(msg.split(","))
            message_ack = ''
            if reponse[1] == 'pi':
                pas_internet = pi(reponse[0])
                transcription = pas_internet.main()

                for keys, values in transcription:
                    message_ack = message_ack + keys + ":" +values +";"

            message_emis = message_ack.encode("utf8")
            self.csocket.send(message_emis)
        print ("Client at ", clientAddress , " disconnected...")
        
LOCALHOST = "192.168.1.5"
PORT = 12101
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(10)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()

