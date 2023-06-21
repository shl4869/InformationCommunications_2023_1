'''
  2071035 Lee Somin
  ETTTP_TicTacToe.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        msg =  self.socket.recv(1024) # get message using socket
        msg = msg.decode()  # decode message

        # check if the message is in format of ETTTP Protocol
        msg_valid_check = check_msg(msg,self.recv_ip) 
        
        if msg_valid_check: # Message is not valid
            # exit game
            self.socket.close()   
            self.quit()
            return
        else:  # If message is valid - send ack, update board and change turn
            ackMsg = make_ack(msg)  # make ACK message
            self.socket.send(ackMsg.encode())   # send encoded ACK message to peer
            msg_split = msg.split() # get array of splitted message
            loc = int(msg_split[3][10])*3+int(msg_split[3][12]) # received next-move
            
        ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        # chek if debug message is in ETTTP format
        if check_msg(d_msg,self.send_ip):
            return
        # split debug message to get the user move position
        d_msg_split = d_msg.split() 
        # convert coordinate position to array location
        user_move = int(d_msg_split[3][10])*3+int(d_msg_split[3][12])
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0:
            return

        # Send move to peer
        self.socket.send(d_msg.encode())
        
        # If ACK is not returned from the peer or it is not valid, exit game
        ackMsg = self.socket.recv(1024)
        ackMsg = ackMsg.decode()
        # if ACK message is not proper, exit game
        if(check_msg(ackMsg,self.recv_ip) or check_ack(d_msg,ackMsg)):
            self.quit()
        
        loc = user_move # peer's move, from 0 to 8

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################

        # send message and check ACK
        msg = 'SEND ETTTP/1.0\r\nHost:'+str(self.send_ip)+'\r\nNew-Move:('+str(row)+','+str(col)+')\r\n\r\n'
        self.socket.send(msg.encode())
        # get ACK message
        ackMsg = self.socket.recv(1024)
        ackMsg = ackMsg.decode()    # decode ACK message
        # if ack message is not proper, this move is not valid
        if(check_msg(ackMsg,self.recv_ip) or check_ack(msg,ackMsg)):
            return False
        # if the function did not return, return true meaning this move is valid
        return True
        ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        ###################  Fill Out  #######################
        # set message informing the winner
        resultMsg = 'RESULT ETTTP/1.0\r\n Host:'+str(self.send_ip)+'\r\nWinner:'+winner+'\r\n\r\n'
        recvMsg = ''
        ackMsg = ''
        
        if get: # if in situation of getting final move
            # recieve result message from peer
            recvMsg = self.socket.recv(1024)
            recvMsg = recvMsg.decode()  # decode message recieved
            # send ack if message is correct
            if check_msg(recvMsg,self.recv_ip):
                return False
            else:
                ackMsg = make_ack(recvMsg)  # generate ack message
                self.socket.send(ackMsg.encode())   # send ack message
                # send result of mine and wait for ack
                self.socket.send(resultMsg.encode())
                ackMsg = self.socket.recv(1024)
                ackMsg = ackMsg.decode()    # decode ack message
                # check if ack recieved is correct
                if(check_msg(ackMsg,self.recv_ip) or check_ack(resultMsg,ackMsg)):
                    return False
            
        else:   # if in situation of sending final move
            # send the result message to peer
            self.socket.send(resultMsg.encode())
            # wait for ack
            ackMsg = self.socket.recv(1024)
            ackMsg = ackMsg.decode()
            # check if ack is correct
            if(check_msg(ackMsg,self.recv_ip) or check_ack(resultMsg,ackMsg)):
                return False
            else:
                # get result message from peer
                recvMsg = self.socket.recv(1024)
                recvMsg = recvMsg.decode()
                # send ack if message is correct
                if check_msg(recvMsg,self.recv_ip):
                    return False
                else:
                    ackMsg = make_ack(recvMsg)  # generate ack message
                    self.socket.send(ackMsg.encode())   # send ack message
        # correct result message should indicate different winner('ME'<->'YOU') for each other
        recvWinner = recvMsg.split()
        if 'Winner:'+winner == recvWinner[3]:
            return False
        return True
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    # split message to check if it is in ETTTP format(starting with "ETTTP/1.0"
    # and to check if the destination of the message equals to reciever ip
    msgSplit = msg.split()
    if(msgSplit[1]== 'ETTTP/1.0' and msgSplit[2] == 'Host:'+str(recv_ip)):
        # return False if there is no problem
        return False
    # return True if there is any problem 
    return True
    ######################################################


def check_ack(msg,ackmsg):
    '''
    Function that checks if recieved ack message is proper
    '''
    # split messages and check if the number of elements are same
    # and if the ack message starts with word "ACK"
    msgSplit = msg.split()
    ackmsgSplit = ackmsg.split()
    # return True if there is any problem
    if(len(msgSplit)!=len(ackmsgSplit) or ackmsgSplit[0]!='ACK'):
        return True
    # check if the message except 'SEND' and 'ACK' is same
    for i in range(1,len(msgSplit)):
        if(msgSplit[i]!=ackmsgSplit[i]):
            return True
    # return Flase if there is no problem
    return False


def make_ack(msg):
    '''
    Function that generates the ack message of given message
    '''
    # split message and substitute the first word 'SEND' with 'ACK'
    msg_split = msg.split()
    ackMsg = 'ACK '
    for i in range(1,len(msg_split)):
        ackMsg+=msg_split[i]+'\r\n'
    ackMsg+='\r\n'
    return ackMsg
