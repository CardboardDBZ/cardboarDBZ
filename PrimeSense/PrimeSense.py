####################
# Class: PrimeSense
# -----------------
# wrapper class for dealing with the primesense
####################
import numpy as np
import scipy as sp
import pandas as pd
import zmq

def print_status(message):
	print '---> %s' % message


class PrimeSense:
	"""
		Class: PrimeSense
		=================
		wrapper class for dealing with the primesense 

		Ideal Operation:
		----------------

			primesense = PrimeSense()
			primesense.send_frames()
	"""

	def __init__(self):

		#=====[ Step 1: setup openni and nite	]=====
		print_status('Initializing OpenNI2')
		openni2.initialize()
		print_status('Initializing NiTE2')
		nite2.initialize(dll_directories=['/Users/jayhack/CS/NI/NiTE2/Redist'])

		#=====[ Step 2: get the device	]=====
		self.device = openni2.Device.open_any()


	def zmq_init(self):
		"""
			initializes zeromq for receiving/sending frames
		"""


if __name__ == '__main__':

	p = PrimeSense()



