import pickle
import random
from DBZHost import DBZController, GestureClassifier, Visualizer

def get_random_pose(pose_dfs_list):
	"""
		returns a random pose 
	"""
	return random.choice(pose_dfs_list)


def visualize_random_pose(visualizer, pose_dfs_list):
	"""
		visualizes a random pose 
	"""
	pose_df = get_random_pose(pose_dfs_list)
	viz.visualize(pose_df)

if __name__ == '__main__':

	gesture_classifier = GestureClassifier(data_dir='../data/')
	print '---> Loading data...'
	gesture_classifier.load_data()
	data = gesture_classifier.data
	pose_df = get_random_pose(data['double_blast'])

	#=====[ Setup Visualizer	]=====
	viz = Visualizer()
	viz.visualize(pose_df)
	



