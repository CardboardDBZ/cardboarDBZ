import pickle
from DBZHost import DBZController

if __name__ == '__main__':

	sample_video = pickle.load(open('../data/twoplayer_test_1.pkl','r'))
	p = DBZController(video=sample_video, data_dir='../data')
	for i in range(len(sample_video) - 2):
		p.update_game()


