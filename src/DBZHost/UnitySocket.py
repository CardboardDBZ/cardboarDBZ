import socket
import json


class UnitySocketGroup:

    def __init__(self, ports=[]):
        self.ports = ports
        self.sockets = [UnitySocket(port) for port in ports]

    def send(self, msg):
        return [socket.send(msg) for socket in self.sockets]

    def close(self):
        return [socket.close() for socket in self.sockets]


class UnitySocket:

    def __init__(self, port=5557):
        self.port = port

        #=====[ Step 1: make sockets ]=====
        self.s = socket.socket()

        #=====[ Step 2: connect ]=====
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setblocking(0)
        self.s.bind(('', self.port))

        self.s.listen(5)
        self.c = None


    def send(self, msg):
        """
            sends the message to both phone and computer
        """
        try:
            self.c, addr = self.s.accept()
        except socket.error:
            if  self.c is None:
                print('#####[ No connection on port ' + str(self.port) + ' detected. ]#####')
                return False
        self.c.sendall(json.dumps(msg))
        return True


    def close(self):
        """
            closes all sockets 
        """
        self.c.close()
        self.s.close()     


