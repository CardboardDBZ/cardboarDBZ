####################
# Class: PrimeSense
# -----------------
# wrapper class for dealing with the primesense
####################
from collections import defaultdict
import numpy as np
import scipy as sp
import pandas as pd
import zmq
from StoppableThread import StoppableThread
from DeviceReceiver import DeviceReceiver
from CommunicationHost import CommunicationHost

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
		self.communication_host = CommunicationHost()

		#=====[ Step 2: set up coordinate lists	]=====
		self.joint_frames = defaultdict(list)



	def key_conversion(self, key_name):
		"""
			ex: JOINT_HEAD_POSITION -> head
		"""
		return '_'.join(key_name.split('_')[1:-1]).lower()


	def get_pos_df(self):
		"""
			sets self.pos_df from self.x_positions... etc

		"""
		dfs = [pd.DataFrame(x) for x in self.joint_frames.values()]
		self.pos_df = pd.concat(dfs, keys=self.joint_frames.keys(), axis=1)


	def update(self):
		frame = self.receiver.get_frame()
		for raw_key in frame.keys():
			if raw_key.endswith('POSITION'):
				key = self.key_conversion(raw_key)
				self.joint_frames[key].append(frame[raw_key])
		self.get_pos_df()


	def record(self):
		print "===[ Press Enter to Start ]==="
		raw_input('--->')
		while True:
			try:
				self.update()
			except KeyboardInterrupt:
				break
		print '===[ Finished Recording ]==='


	def person_exists(self):
		"""
			returns true if there is a person onscreen in the last 
			frame in self.pos_df
			criterion: all *positions* are non-null
		"""
		return self.pos_df.iloc[-1].isnull().sum() == 0


	def coordinate_transform(self, c_coords):
		"""
			given a position df, this will return 
			it transformed

			kinect_coords: df of coordinates from the primesense's 
				perspective

			Uses convention: c = camera, h = human

		"""
		assert type(c_coords) == pd.DataFrame
		origin = (c_coords.left_shoulder + c_coords.right_shoulder)/2.
		x_axis = c_coords.right_shoulder - origin
		z_axis = origin - c_coords.torso
		y_axis = pd.DataFrame(np.cross(z_axis, x_axis), columns=['x','y','z'])

		#=====[ d = difference of points from origin	]=====
		differences = [c_coords[label] - origin for label in c_coords.columns.levels[0]]
		d = pd.concat(differences, keys=c_coords.columns.levels[0], axis=1)
		return origin, x_axis, y_axis, z_axis, d

		





if __name__ == '__main__':

	p = PrimeSense()



