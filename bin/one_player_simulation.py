import pickle
from DBZHost import DBZController

if __name__ == '__main__':

	sample_video = pickle.load(open('../data/lucas_vs_brandon.vid','r'))
	controller = DBZController(num_players=2, video=sample_video, data_dir='../data')
	for i in range(len(sample_video) - 2):
		controller.update_game()


