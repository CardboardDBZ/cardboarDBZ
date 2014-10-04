####################
# Class: PrimeSense
# -----------------
# wrapper class for dealing with the primesense
####################
import numpy as np
import scipy as sp
import pandas as pd
import zmq
from StoppableThread import StoppableThread
from DeviceReceiver import DeviceReceiver

def print_status(message):
	print '---> %s' % message


class PrimeSense():
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

		#=====[ Step 1: setup receiving data	]=====
		self.receiver = DeviceReceiver('primesense')

		#=====[ Step 2: set up coordinate lists	]=====
		self.x_positions = []
		self.y_positions = []
		self.z_positions = []


	def key_conversion(self, key_name):
		"""
			ex: JOINT_HEAD_POSITION -> head
		"""
		return '_'.join(key_name.split('_')[1:-1]).lower()


	def update(self):
		frame = self.receiver.get_frame()
		x, y, z = {}, {}, {}
		for raw_key in frame.keys():
			if raw_key.endswith('POSITION'):
				key = self.key_conversion(raw_key)
				x[key] = frame[raw_key]['x']
				y[key] = frame[raw_key]['y']
				z[key] = frame[raw_key]['z']								
		self.x_positions.append(x)
		self.y_positions.append(y)
		self.z_positions.append(z)


	def get_pose_df(self):
		"""
			sets self.pose_df from self.x_positions... etc
		"""
		#=====[ Step 1: make individual dfs	]=====
		x_df = pd.DataFrame(self.x_positions)
		y_df = pd.DataFrame(self.y_positions)
		z_df = pd.DataFrame(self.z_positions)
		assert len(x_df) == len(y_df)
		assert len(z_df) == len(x_df)

		#=====[ Step 2: join	]=====
		self.pose_df = pd.concat([x_df, y_df, z_df], keys=['x','y','z'], axis=1)




	def zmq_init(self):
		"""
			initializes zeromq for receiving/sending frames
		"""
		pass


if __name__ == '__main__':

	p = PrimeSense()



