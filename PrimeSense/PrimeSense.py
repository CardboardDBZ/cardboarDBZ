####################
# Class: PrimeSense
# -----------------
# wrapper class for dealing with the primesense
####################
import os
import pickle
from copy import copy
import numpy as np
import scipy as sp
import pandas as pd
import zmq

from StoppableThread import StoppableThread
from DeviceReceiver import DeviceReceiver
from CommunicationHost import CommunicationHost
from Player import Player


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

	def __init__(self, video=None):

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
		self.init_game ()



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
			self.print_game_state()
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


	def init_game(self):
		"""
			Tries to initialize the two players; won't do so 
			until there are at least two players present
		"""
		self.game_started = False
		self.players = [None, None]
		self.update_skeletons()

		#=====[ Step 1: loop until we see two players	]=====
		while (self.num_skeletons < 2):
			self.update_skeletons()

		#=====[ Step 2: initialize the two players	]=====
		head_coords = [c_coords['head']['x'] for c_coords in self.skeleton_poses_c]
		leftmost_player_ix = np.argmin(head_coords) #we THINK this gets the leftmost
		rightmost_player_ix = np.argmax(head_coords)
		print leftmost_player_ix, rightmost_player_ix
		print head_coords
		self.players[0] = Player(self.skeleton_poses_c[leftmost_player_ix])
		self.players[1] = Player(self.skeleton_poses_c[rightmost_player_ix])


	def update_players(self):
		"""
			for each player, this will have them choose the 
			best new location for their skeleton 
		"""
		skeleton_c_coords = copy(self.skeleton_poses_c)
		for player in self.players:
			player.update(skeleton_c_coords)


	def update_game(self):
		"""
			updates all player locations in the game;
		"""
		self.update_skeletons()
		self.update_players()
		self.print_game_state()
		# self.notify_players() #TODO


	def print_game_state(self):
		"""
			prints out what is going on in the game currently
		"""
		print '##################################################'
		print '##########[ FRAME STATS ]#########################'
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
			except KeyboardInterrupt:
				break
		print '===[ Finished Recording ]==='
		print "ENTER SAVE NAME: (in ./data/)"
		save_name = raw_input('--> ')
		pickle.dump(raw_frames, open(os.path.join('./data', 'save_name'), 'w'))
		return raw_frames




if __name__ == '__main__':

	p = PrimeSense()



