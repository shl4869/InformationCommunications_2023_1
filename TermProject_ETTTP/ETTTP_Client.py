'''
  2071035 Lee Somin
  ETTTP_Client.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg, check_ack, make_ack
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server
        # send IP of self to server
        client_socket.send(MY_IP.encode())
        # recieve information about starting user
        startMsg = client_socket.recv(1024)
        startMsg = startMsg.decode()
        # check if the start message is proper
        if check_msg(startMsg,MY_IP):
            client_socket.close()
        # split message and check who is the first player
        startMsgSplit = startMsg.split()
        start = -1
        if startMsgSplit[3] == 'First-Move:ME':
            start = 0
        elif startMsgSplit[3] == 'First-Move:YOU':
            start = 1
        else:
            client_socket.close()
    
        ######################### Fill Out ################################
        # Send ACK
        ackMsg = make_ack(startMsg)
        client_socket.send(ackMsg.encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        
