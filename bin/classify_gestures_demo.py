#!/Users/jayhack/anaconda/bin/python
import argparse
from DBZHost import DBZController

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
	dbz_controller = DBZController(debug=True)
	while True:
		try:
			dbz_controller.update_no_game()
			print dbz_controller.players[0].gesture
		except KeyboardInterrupt:
			break
	print 'HERE'
