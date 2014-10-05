#!/Users/jayhack/anaconda/bin/python
import argparse
from PrimeSense import PrimeSense

if __name__ == '__main__':

	#==========[ ARGPARSING	]==========
	parser = argparse.ArgumentParser()
	parser.add_argument(	'-c', '--classifier_name',
							metavar='O', type=str, nargs=1, dest='classifier_name', required=False,
							default='clf.pkl', help='path to output directory (local filesystem)', 
							action='store')
	args = parser.parse_args ()
	classifier_name = args.classifier_name[0]

	#==========[ CREATE USER TRACKER, GESTURE CLASSIFIER	]==========
	primesense = PrimeSense()
	while True:
		primesense.update_no_game()
		print primesense.players[0].gesture

