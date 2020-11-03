# import jpysocket

# host='localhost' #Host Name
# port=12345    #Port Number
# s=jpysocket.jpysocket() #Create Socket
# s.connect((host,port)) #Connect to socket
# print("Socket Is Connected....")
# msgrecv=s.recv(1024) #Recieve msg
# msgrecv=jpysocket.jpydecode(msgrecv) #Decript msg
# print("From Server: ",msgrecv) # Client receive message from server.
# msgsend=jpysocket.jpyencode("Ok Boss.") #Encript The Msg, Client send message to server
# s.send(msgsend) #Send Msg
# s.close() #Close connection
# print("Connection Closed.")

import socket

HEADERSIZE = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1242))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(1024) # รับค่า
        msg = msg.decode("utf-8")
        print(msg)
        # if new_msg:
        #     print("new msg len:",msg[:HEADERSIZE])
        #     msglen = (msg[:HEADERSIZE])
        #     new_msg = False

        # print(f"full message length: {msglen}")

        # full_msg += msg.decode("utf-8")

        # print(len(full_msg))


        # if len(full_msg)-HEADERSIZE == msglen:
        #     print("full msg recvd")
        #     print(full_msg[HEADERSIZE:])
        #     new_msg = True
        #     full_msg = ""


            
# while True:
#     full_msg = ''
#     new_msg = True
#     while True:
#         msg = s.recv(16) # รับค่า
#         if new_msg:
#             print("new msg len:",msg[:HEADERSIZE])
#             msglen = int(msg[:HEADERSIZE])
#             new_msg = False

#         print(f"full message length: {msglen}")

#         full_msg += msg.decode("utf-8")

#         print(len(full_msg))


#         if len(full_msg)-HEADERSIZE == msglen:
#             print("full msg recvd")
#             print(full_msg[HEADERSIZE:])
#             new_msg = True
#             full_msg = ""
