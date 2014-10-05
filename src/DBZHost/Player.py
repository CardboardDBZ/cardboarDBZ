####################
# Class: Player
# -------------
# wrapper class for representing a single Player
####################
import numpy as np 
import scipy as sp
from scipy.stats import mode
import pandas as pd
from UnitySocket import UnitySocket
from GestureClassifier import GestureClassifier

class Player:
	"""
		Ideal Operation:
		----------------
		- at startup, initializes itself with an origin
		- has a moving origin that it tracks
	"""
	DISTANCE_THRESHOLD = 500.
	SCALING_CONSTANT = 400.
	GESTURE_LENGTH = 15


	def __init__(self, index, gesture_classifier):
		"""
			intializes this player's coordinates
		"""
		self.socket = UnitySocket(index)
		self.index = index
		self.gesture_classifier = gesture_classifier
		self.c_coords = None
		self.h_coords = None
		self.gesture = 'no_gesture'
		self.gesture_history = []
		self.state_history = []


	def get_origin(self, c_coords):
		"""
			given a skeleton in c_coords, this will return its origin 
		"""
		return np.array((c_coords['left_shoulder'] + c_coords['right_shoulder'])/2.)


	def get_origin_axes(self, c_coords):
		"""
			given this player's c_coords, this will set self.:
				origin
				x/y/z_axis
		"""
		self.origin = self.get_origin(c_coords)
		x_axis = np.array(c_coords['right_shoulder'] - self.origin)
		z_axis = np.array(self.origin - c_coords['torso'])
		y_axis = np.cross(z_axis, x_axis)
		self.x_axis = x_axis / np.linalg.norm(x_axis)
		self.y_axis = y_axis / np.linalg.norm(y_axis)
		self.z_axis = z_axis / np.linalg.norm(z_axis)


	def c_coords_to_h_coords(self, c_coords):
		"""
			converts c_coords to this player's coordinate system 
			(h_coords)

		"""
		#=====[ Step 1: get differences	]=====
		differences = c_coords.copy()
		for label in c_coords.columns:
			differences[label] = differences[label] - self.origin

		#=====[ Step 2: transform each one	]=====
		M = np.eye(3)
		M[:, 0], M[:,1], M[:,2] = self.x_axis, self.y_axis, self.z_axis
		# M*[a, b, c] = d
		# ==> pinv(M)*d = [a, b, c]
		h_coords = differences.copy()
		for label in h_coords.columns:
			h_coords[label] = np.dot(np.linalg.pinv(M), h_coords[label])
		return h_coords


	def update_coords(self, new_c_coords):
		"""
			sets all coordinates, assuming new_c_coords is the new 
			position in camera coordinates
		"""
		self.c_coords = new_c_coords
		self.get_origin_axes(self.c_coords)
		self.h_coords = self.c_coords_to_h_coords(self.c_coords)


	def get_similarity(self, c_coords):
		"""
			returns the similarity between this skeleton and the one passed in,
			represented with c_coords 
		"""
		origin_other = self.get_origin(c_coords)
		return np.linalg.norm(np.array(self.origin) - np.array(origin_other))


	def update(self, skeleton_c_coords):
		"""
			skeleton_c_coords: list of c_coords of skeletons, passed in 
				from parent PrimeSense object

			this will pick the one out that most likely corresponds to 
			this player; it will then update its own coordinates 
			accordingly and *REMOVE* the corresponding coords from its own
			frame
		"""
		if len(skeleton_c_coords) == 0:
			return #no update

		if type(self.c_coords) == type(None):
			self.update_coords(skeleton_c_coords.pop(0))
			self.update_gesture()
			return


		distances = [self.get_similarity(c_coords) for c_coords in skeleton_c_coords]
		if not min(distances) < self.DISTANCE_THRESHOLD:
			return #no update

		else:
			best_ix = np.argmin(distances)
			self.update_coords(skeleton_c_coords.pop(best_ix)) #update with best
			self.update_gesture()


	def update_gesture(self):
		"""
			sets self.gesture to the prediction of self.gesture_classifier 
		"""
		if type(self.h_coords) != type(None) :
			self.gesture_history.append(self.gesture_classifier.predict(self.h_coords)[0])

		if len(self.gesture_history) > 0:
			self.gesture = mode(self.gesture_history[-15:])[0][0]

		#=====[ Get direction	]=====
		if self.gesture == 'right_blast':
			self.direction = self.c_coords['right_hand'] - self.c_coords['right_elbow']
		elif self.gesture == 'left_blast':
			self.direction = self.c_coords['right_hand'] - self.c_coords['right_elbow']			
		elif self.gesture == 'double_blast':
			self.direction = (self.c_coords['right_hand'] + self.c_coords['left_hand'])/2 - self.c_coords['torso']
		else:
			self.direction = None



	def format_coordinates(self, coords):
		"""
			given coordinates as a pandas series, this will format them
			for sending to the phone 
		"""
		coords = coords.copy()
		coords = coords / float(self.SCALING_CONSTANT)
		# coords.index = ['z', 'y', 'x']
		return coords.to_dict()



	def send_state(self, opponent):
		"""
			sends this Player's state from the primesense to the 
			actual player via UnitySocket 
		"""
		message = {}

		#=====[ Step 1: self	]=====
		message['self_coords'] = self.format_coordinates(self.c_coords)
		message['self_gesture'] = self.gesture
		if not self.direction is None:
			message['self_direction'] = self.format_coordinates(self.direction)

		#=====[ Step 2: other	]=====
		if not opponent is None:
			message['opponent_coords'] = self.format_coordinates(opponent.c_coords)
			message['opponent_gesture'] = opponent.gesture
			if not opponent.direction is None:
				message['opponent_direciton'] = self.format_coordinates(opponent.direction)

		print message, '\n\n'
		self.state_history.append(message)
		self.socket.send(message)


	def __str__ (self):
		"""
			returns a string representation of the current player 
		"""
		return 'c_coords: \n' + str(self.c_coords)




