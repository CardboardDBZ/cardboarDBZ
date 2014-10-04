#-------------------------------------------------- #
# Class: CommunicationHost
# ------------------------
# Takes care of sending data over TCP ports to 
# the listener phones
#-------------------------------------------------- #
import zmq

class CommunicationHost:

	def __init__(self):
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.PUB)
		self.socket.bind("tcp://*:5556")

	def send_frame(self, frame):
		assert type(frame) == dict
		socket.send_json(frame)
