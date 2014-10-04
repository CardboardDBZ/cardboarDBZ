####################
# Class: PrimeSense
# -----------------
# wrapper class for dealing with the primesense
####################
import numpy as np
import scipy as sp
import pandas as pd
import primesense
from primesense import openni2, nite2

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
		nite2.initialize()


if __name__ == '__main__':

	p = PrimeSense()

