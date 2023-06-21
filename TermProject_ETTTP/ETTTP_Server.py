'''
  2071035 Lee Somin
  ETTTP_Sever.py
 
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
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
                
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        CLIENT_IP = client_socket.recv(1024)    #recive IP address of client from client
        CLIENT_IP = CLIENT_IP.decode()  # decode the IP message
        first_move = 'ME' if start == 0 else 'YOU' # if random number is 0, server goes first, and if number is 1, client goes first
        startMsg = 'SEND ETTTP/1.0\r\nHost:'+str(CLIENT_IP)+'\r\nFirst-Move:'+ first_move + '\r\n\r\n'
        client_socket.send(startMsg.encode())
    
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        ackMsg = client_socket.recv(1024)
        ackMsg = ackMsg.decode()
        # if message and ack is not valid, exit game
        if(check_msg(ackMsg,MY_IP) or check_ack(startMsg,ackMsg)):
            client_socket.close()
            break
        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()
