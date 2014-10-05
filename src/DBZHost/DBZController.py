######################
# Class: DBZController
# --------------------
# wrapper class for dealing with all things cardboarDBZ.
######################
import os
import pickle
from copy import copy
import numpy as np
import scipy as sp
import pandas as pd
import zmq
import hashlib
import time

from StoppableThread import StoppableThread
from DeviceReceiver import DeviceReceiver
from CommunicationHost import CommunicationHost
from Player import Player
from GestureClassifier import GestureClassifier


def print_status(message):
	print '---> %s' % message


class DBZController():
	"""
		Class: DBZController
		====================
		wrapper class for dealing with the primesense 

		Ideal Operation:
		----------------

			primesense = PrimeSense()
			primesense.send_frames()

			p.skeleton_poses: list of dfs representing poses in c_coords 
			p.skeleton_poses_h: list of dfs reprsenting poses in h_coords
	"""

	def __init__(self, data_dir='../data', video=None, debug=False):
		self.data_dir = data_dir
		self.debug = debug

		#=====[ Step 1: setup receiving data	]=====
		if video:
			self.video = video			
			self.video_mode = True
			self.video_frame = -1
		else:
			self.receiver = DeviceReceiver('primesense')
			self.video_mode = False

		#=====[ Step 2: setup communication	]=====
		self.communication_host = CommunicationHost()

		#=====[ Step 3: try to inialize the game	]=====
		self.init_players()
		if not self.debug:
			self.init_game ()





	################################################################################
	####################[ SKELETONS/DEVICES]########################################
	################################################################################

	def key_conversion(self, key_name):
		"""
			ex: JOINT_HEAD_POSITION -> head
		"""
		return '_'.join(key_name.split('_')[1:-1]).lower()


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


	def update_skeletons(self, input_frame=None):
		"""
			updates the following variables:
				- frame_raw: raw json 
				- num_skeletons: # of skeletons
				- frame_processed: cleaned json
				- skeleton_poses_c: list of dataframes containing skeleton poses (c_coords)
				- skeleton_poses_h: list of dataframes containing skeleton poses (h_coords)
		"""
		#=====[ Step 1: deal with video mode	]=====
		if not input_frame and self.video_mode:
			self.video_frame += 1
			raw_input('Video Mode [%s]: press enter to continue to next frame' % self.video_frame)
			self.update_skeletons(input_frame=self.video[self.video_frame])
			# self.print_game_state()
			return

		#=====[ Step 2: figure out what the input frame is	]=====
		if input_frame:
			self.frame_raw = input_frame
		else:
			self.frame_raw = self.receiver.get_frame()
		self.num_skeletons = len(self.frame_raw.keys())

		#=====[ Step 3: process the frame	]=====
		self.frame_processed = {}
		for s_name, s_frame in self.frame_raw.iteritems():
			self.frame_processed[s_name] = {}
			for raw_key in s_frame.keys():
				if raw_key.endswith('POSITION'):
					key = self.key_conversion(raw_key)
					self.frame_processed[s_name][key] = s_frame[raw_key]

		#=====[ Step 4: get skeleton_poses	]=====
		self.skeleton_poses_c = []
		for s_name, s_frame in self.frame_processed.items():
			self.skeleton_poses_c.append(self.dict_to_df(s_frame))







	################################################################################
	####################[ GAME AND PLAYERS ]########################################
	################################################################################

	def init_players(self):
		"""
			initializes players 
		"""
		self.gesture_classifier = GestureClassifier(data_dir=self.data_dir)
		self.gesture_classifier.load_classifier()
		self.players = [Player(0, self.gesture_classifier), Player(1, self.gesture_classifier)]
		self.update_skeletons()


	def init_game(self):
		"""
			Tries to initialize the two players; won't do so 
			until there are at least two players present
		"""
		self.game_started = False
		self.update_skeletons()

		#=====[ Step 1: loop until we see two players	]=====
		while (self.num_skeletons < 2):
			self.update_skeletons()

		#=====[ Step 2: initialize the two players	]=====
		self.players[0].update(self.skeleton_poses_c)
		self.players[1].update(self.skeleton_poses_c)


	def update_players(self):
		"""
			for each player, this will have them choose the 
			best new location for their skeleton 
		"""
		skeleton_c_coords = copy(self.skeleton_poses_c)
		for player in self.players:
			player.update(skeleton_c_coords)


	def send_player_states(self):
		"""	
			sends the states of players from Player objects to 
			the actual phones 
		"""
		if self.players[0] and self.players[1]:
			self.players[0].send_state(self.players[1])
			self.players[1].send_state(self.players[0])			


	def update_game(self):
		"""
			updates all player locations in the game;
		"""
		self.update_skeletons()
		self.update_players()
		self.print_game_state()
		self.send_player_states()


	def update_no_game(self):
		"""
			does updates but doesn't assume the game is going 
			on 
		"""
		self.update_skeletons()
		self.update_players()



	def print_game_state(self):
		"""
			prints out what is going on in the game currently
		"""
		print '\n\n##################################################'
		print '##########[ FRAME STATS: #%d ]#####################' % self.video_frame
		print '##################################################'				
		print '# skeletons in frame: %d' % self.num_skeletons

		print '\n=====[ PLAYER 1	]====='
		print self.players[0]

		print '\n=====[ PLAYER 2	]====='
		print self.players[1]



	def record(self):
		print "===[ Press Enter to Start ]==="
		raw_input('--->')
		raw_frames = []
		while True:
			try:
				self.update_skeletons()
				raw_frames.append(self.frame_raw)
				print '.'
			except KeyboardInterrupt:
				break
		print '===[ Finished self.debuging ]==='
		print "ENTER SAVE NAME: (in ./data/)"
		save_name = raw_input('--> ')
		pickle.dump(raw_frames, open(os.path.join(self.data_dir, save_name), 'w'))
		return raw_frames


	def record_gesture(self):

		print '===[ self.debug Gesture ]==='
		print "Enter gesture name"
		gesture_name = raw_input('--->')
		
		#=====[ Step 1: make a gesture directory	]=====
		gestures_dir = os.path.join(self.data_dir, 'gestures')
		gesture_dir = os.path.join(gestures_dir, gesture_name)
		if not os.path.exists(gesture_dir):
			os.mkdir(gesture_dir)

		#=====[ Step 2: self.debug each gesture	]=====
		player = self.players[0]
		while True:
			try:
				raw_input('>> press enter to self.debug a gesture <<')
				self.update_skeletons()
				if self.num_skeletons != 1:
					print "==> ERROR: multiple people on premises"
					continue 
				
				print self.skeleton_poses_c[0]
				player.update(self.skeleton_poses_c)

				h_coords = player.h_coords
				c_coords = player.c_coords
				coords = {'c_coords':c_coords, 'h_coords':h_coords}
				filename = hashlib.md5(str(time.time())).hexdigest() + '.pose'
				pickle.dump(coords, open(os.path.join(gesture_dir, filename), 'w'))
				print "[[ SAVED: %s ]]" % os.path.join(gesture_dir, filename)
			except KeyboardInterrupt:
				break





if __name__ == '__main__':

	p = PrimeSense()



