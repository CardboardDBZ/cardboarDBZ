#-------------------------------------------------- #
# Class: Visualizer
# -----------------
# class for creating visualizations of body poses
#-------------------------------------------------- #
#==========[ Matplotlib tools	]==========
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, RadioButtons


class Visualizer:
	"""
		Class: Visualizer
		=================
		Visualizer for data received from the Primesense 

		Ideal Operation:
		----------------
		visualizer.visualize(pose_df)

	"""

	limb_joint_pairs = 	[
							('head', 'neck'),
							('neck', 'left_shoulder'),
							('neck', 'right_shoulder'),
							('left_shoulder', 'left_elbow'),
							('right_shoulder', 'right_elbow'),
							('left_elbow', 'left_hand'),
							('right_elbow', 'right_hand'),
							('neck', 'torso'),
							('torso', 'left_hip'),
							('torso', 'right_hip'),
							('left_hip', 'left_knee'),
							('right_hip', 'right_knee'),
							('left_knee', 'left_foot'),
							('right_knee', 'right_foot')
						]


	def __init__ (self):
		"""
			PUBLIC: Constructor
			-------------------
			creates all static aspects of the plot
		"""
		#=====[ Create figure/axes	]=====
		self.fig 			= plt.figure (figsize=plt.figaspect(1)*1.5)
		self.ax 			= Axes3D (self.fig, rect=[0, 0.2, 1, 0.8], axisbg='#B0B0B0')
		self.ax.set_xticks([])
		self.ax.set_yticks([])
		self.ax.set_zticks([])


		# self.ax_progress 	= plt.axes([0, 0, 1, 0.1], axisbg='#B0B0B0')
		# self.ax_play	 	= plt.axes([0, 0.1, 0.5, 0.1])
		# self.ax_mark	 	= plt.axes([0.5, 0.1, 0.5, 0.1])		
		# self.ax.set_zticks ([])


	# def get_pose_limits (self, pose_df):
	# 	"""	
	# 		returns centroid, x_lims, y_lims, z_lims
	# 	"""
	# 	centroid = pose_df.mean(axis=1)
	# 	x_lims = pose_df.loc['x'].min(), pose_df.loc['x'].max()
	# 	y_lims = pose_df.loc['y'].min(), pose_df.loc['y'].max()
	# 	z_lims = pose_df.loc['z'].min(), pose_df.loc['z'].max()				
	# 	return centroid, x_lims, y_lims, z_lims


	# def shift (self, pose_df, origin):
	# 	"""
	# 		PRIVATE: shift
	# 		--------------
	# 		given a frame, shifts it to the provided origin
	# 	""" 
	# 	return {	
				
	# 				k:	{	
	# 						'x':v['x'] - origin[0], 
	# 						'y':v['y'] - self.y_floor,
	# 						'z':v['z'] - origin[2]	
	# 					} 
					
	# 					for k, v in joint_coords.items ()
	# 			}


	# def init_plot (self, pose_df):
	# 	"""
	# 		sets plot aspect ratio and bounds such that the body
	# 		actually looks like a body; sets colors
	# 	"""
	# 	#==========[ Step 1: get centroid/limits for all dimensions ]==========
	# 	# self.centroid, self.x_lims, self.y_lims, self.z_lims = self.get_pose_limits (pose_df)
	# 	# self.z_floor = -640

	# 	# #==========[ Step 2: set limits ]==========
	# 	# self.ax.set_xlim (self.x_lims)
	# 	# self.ax.set_ylim (self.y_lims)		
	# 	# self.ax.set_zlim (0, self.z_lims[1] - self.z_lims[0])

	# 	#==========[ Step 3: set aspect ratio	]==========
	# 	# x_span = self.x_lims[1] - self.x_lims[0]
	# 	# y_span = self.y_lims[1] - self.y_lims[0]
	# 	# z_span = self.z_lims[1] - self.z_lims[0]

	# 	# self.ax.set_aspect (x_span/z_span)



	####################################################################################################
	##############################[ --- DRAWING ON PLOT --- ]###########################################
	####################################################################################################

	def plot_line (self, p1, p2):
		"""
			PRIVATE: plot_line
			------------------
			given two points, plots a line between them
			necessary because matplotlib screws up the axes for us...
		"""
		xs = [p1['x'], p2['x']]
		ys = [p1['y'], p2['y']]
		zs = [p1['z'], p2['z']]
		return self.ax.plot (xs, ys, zs, color='#780000', linewidth=4, marker='o', markersize=12)


	def visualize(self, pose_df):
		"""
			draws the pose on the figure 
		"""
		self.ax.set_aspect(1)
		for j1_name, j2_name in self.limb_joint_pairs:
			self.plot_line(pose_df[j1_name], pose_df[j2_name])
		plt.xlabel('X')
		plt.ylabel('Y')
		plt.show()


