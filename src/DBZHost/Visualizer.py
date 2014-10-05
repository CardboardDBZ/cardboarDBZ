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
		pass


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
		#=====[ Create figure/axes	]=====
		self.fig 			= plt.figure (figsize=plt.figaspect(1)*1.5)
		self.ax 			= Axes3D (self.fig, axisbg='#B0B0B0')
		self.ax.set_xticks([])
		self.ax.set_yticks([])
		self.ax.set_zticks([])
		# self.ax.set_aspect(1)

		#=====[ Draw	]=====
		for j1_name, j2_name in self.limb_joint_pairs:
			self.plot_line(pose_df[j1_name], pose_df[j2_name])
		plt.xlabel('X')
		plt.ylabel('Y')





