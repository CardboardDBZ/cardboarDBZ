import socket
import json

COMPUTER_PORT = 5557
# PHONE_PORT = 5558

class UnitySocket:

    def __init__(self, player=0):
        self.player = player

        #=====[ Step 1: get port numbers ]=====
        self.port_computer = COMPUTER_PORT
        # self.port_phone = PHONE_PORT + player

        #=====[ Step 2: make sockets ]=====
        self.s_computer = socket.socket()
        # self.s_phone = socket.socket()

        #=====[ Step 3: connect ]=====
        self.s_computer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_computer.setblocking(0)
        self.s_computer.bind(('', self.port_computer))

        # self.s_phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.s_phone.setblocking(0)
        # self.s_phone.bind(('', self.port_phone))

        self.s_computer.listen(5)
        self.c_computer = None
        # self.s_phone.listen(5)
        # self.c_phone = None


    def send(self, msg):
        """
            sends the message to both phone and computer
        """
        try:
            self.c_computer, addr_computer = self.s_computer.accept()
            # self.c_phone, addr_phone = self.s_phone.accept()            
        except socket.error:
            if  self.c_computer is None:
                print('Player #' + str(self.player) + ' is not connected.')
                return False
        self.c_computer.sendall(json.dumps(msg))
        # self.c_phone.sendall(json.dumps(msg))
        return True


    def close(self):
        """
            closes all sockets 
        """
        self.c_computer.close()
        self.s_computer.close()

        # self.c_phone.close()
        # self.s_phone.close()        


