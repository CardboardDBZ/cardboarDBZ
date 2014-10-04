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

		#=====[ Get axes (normalized) and origin	]=====
		origin = (c_coords.left_shoulder + c_coords.right_shoulder)/2.
		x_axis = c_coords.right_shoulder - origin
		z_axis = origin - c_coords.torso
		y_axis = pd.DataFrame(np.cross(z_axis, x_axis), columns=['x','y','z'])
		x_axis = x_axis.divide(x_axis.sum(axis=1), axis=0)
		y_axis = y_axis.divide(y_axis.sum(axis=1), axis=0)
		z_axis = z_axis.divide(z_axis.sum(axis=1), axis=0)

		#=====[ get d = difference of points from origin	]=====
		differences = [c_coords[label] - origin for label in c_coords.columns.levels[0]]
		d = pd.concat(differences, keys=c_coords.columns.levels[0], axis=1)

		#=====[ rephrase d using the basis x_axis, y_axis, z_axis	]=====
		H = []
		for ix, row in c_coords.iterrows():
			M = np.eye(3)
			M[:, 0] = np.array(x_axis.iloc[ix])
			M[:, 1] = np.array(y_axis.iloc[ix])
			M[:, 2] = np.array(z_axis.iloc[ix])
			# M*[a, b, c] = d
			# ==> pinv(M)*d = [a, b, c]
			h_coords = [np.dot(np.linalg.pinv(M), np.array(d.iloc[ix][label])) for label in c_coords.columns.levels[0]]
			h_coords = [pd.DataFrame([h], columns=['x','y','z']) for h in h_coords]
			h_coords = pd.concat(h_coords, keys=c_coords.columns.levels[0], axis=1)
			H.append(h_coords)
		H = pd.concat(H)

		return origin, x_axis, y_axis, z_axis, H


		





if __name__ == '__main__':

	p = PrimeSense()



