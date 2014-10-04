import socket
import json

class UnitySocket:

    def __init__(self, player=0):
        self.player = player
        self.port = 5557 + player
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setblocking(0)
        self.s.bind(('', self.port))
        self.s.listen(5)
        self.c = None

    def send(self, msg):
        print msg, '\n\n\n'
        try:
            self.c, addr = self.s.accept()
        except socket.error:
            if self.c is None:
                print('Player #' + str(self.player) + ' is not connected.')
                return False
        self.c.sendall(json.dumps(msg))
        return True

    def close(self):
        self.c.close()
        self.s.close()
