import pickle
import argparse
from DBZHost import DBZController

if __name__ == '__main__':

	sample_video = pickle.load(open('../data/jay_alone.vid','r'))
	controller = DBZController(num_players=1, video=sample_video, data_dir='../data')
	
	parser = argparse.ArgumentParser()
	parser.add_argument(	'-r', '--realtime',
							metavar='O', type=bool, nargs=1, dest='realtime', required=False,
							default=False, help='wether to do real time or not', 
							action='store')
	args = parser.parse_args ()
	realtime = args.realtime[0]
	print realtime

	for i in range(len(sample_video) - 2):
		controller.update_game(realtime=realtime)


