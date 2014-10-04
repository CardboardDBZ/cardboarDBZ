#-------------------------------------------------- #
# Class: CommunicationHost
# ------------------------
# Takes care of sending data over TCP ports to 
# the listener phones
#-------------------------------------------------- #
import zmq

class CommunicationHost:

	def __init__(self):
		self.context = zmq.context()
		self.socket = context.socket(zmq.PUB)
		socket.bind("tcp://*:5556")

	def send_frame(self, frame):
		assert type(frame) == dict
		socket.send(frame)
