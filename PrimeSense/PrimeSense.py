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

			p.skeleton_poses: list of dfs representing poses in c_coords 
			p.skeleton_poses_h: list of dfs reprsenting poses in h_coords
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


	def dict_to_df(self, d):
		"""
			performs the following conversion:
				{	
					joint_name:{'x':..., 'y':..., 'z':...},
					..
				}
				==>
				df indexed by joint_name -> coordinate 
		"""

		return pd.DataFrame(d)


	def update(self, input_frame=None):
		"""
			- updates frame_processed (primesense coordinates)
		"""
		#=====[ Step 1: raw frame and metadata	]=====
		if input_frame:
			self.frame_raw = input_frame
		else:
			self.frame_raw = self.receiver.get_frame()
		self.num_skeletons = len(self.frame_raw.keys())

		#=====[ Step 2: process the frame	]=====
		self.frame_processed = {}
		for s_name, s_frame in self.frame_raw.iteritems():
			self.frame_processed[s_name] = {}
			for raw_key in s_frame.keys():
				if raw_key.endswith('POSITION'):
					key = self.key_conversion(raw_key)
					self.frame_processed[s_name][key] = s_frame[raw_key]

		#=====[ Step 3: get skeleton_poses	]=====
		self.skeleton_poses_c = []
		for s_name, s_frame in self.frame_processed.items():
			self.skeleton_poses_c.append(self.dict_to_df(s_frame))

		#=====[ Step 4: get skeleton_poses_h	]=====
		self.skeleton_poses_h = [self.to_human_coords(c_coords) for c_coords in self.skeleton_poses_c]



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



	def get_origin_axes(self, c_coords):
		"""
			given a body represented in camera coordinates,
			returns its origin,x,y,z_axes

			c_coords: pd.DataFrame containing camera coordinates
			returns: numpy arrays for origin, x/y/z axes
		"""
		origin = np.array((c_coords['left_shoulder'] + c_coords['right_shoulder'])/2.)
		x_axis = np.array(c_coords['right_shoulder'] - origin)
		z_axis = np.array(origin - c_coords['torso'])
		y_axis =np.cross(z_axis, x_axis)
		x_axis = x_axis / x_axis.sum()
		y_axis = y_axis / y_axis.sum()
		z_axis = z_axis / z_axis.sum()
		return origin, x_axis, y_axis, z_axis


	def convert_coordinate_system(self, original_coords, origin, x_axis, y_axis, z_axis):
		"""
			converts original_coords to the coordinate system 
			represented by origin, x_axis, y_axis, z_axis. each of those 
			are in the original cooords.

		"""
		#=====[ Step 1: get differences	]=====
		differences = original_coords.copy()
		for label in original_coords.columns:
			differences[label] = differences[label] - origin

		#=====[ Step 2: transform each one	]=====
		M = np.eye(3)
		M[:, 0], M[:,1], M[:,2] = x_axis, y_axis, z_axis
		# M*[a, b, c] = d
		# ==> pinv(M)*d = [a, b, c]
		new_coords = differences.copy()
		for label in new_coords.columns:
			new_coords[label] = np.dot(np.linalg.pinv(M), new_coords[label])
		return new_coords


	def to_human_coords(self, camera_coords):
		"""
			given a position df, this will return 
			it transformed

			kinect_coords: df of coordinates from the primesense's 
				perspective

			Uses convention: c = camera, h = human

		"""
		origin, x_axis, y_axis, z_axis = self.get_origin_axes(camera_coords)
		return self.convert_coordinate_system(camera_coords, origin, x_axis, y_axis, z_axis)


		





if __name__ == '__main__':

	p = PrimeSense()



