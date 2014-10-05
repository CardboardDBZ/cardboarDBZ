#!/Users/jayhack/anaconda/bin/python
import argparse
from GestureClassifier import GestureClassifier

if __name__ == '__main__':

	#==========[ ARGPARSING	]==========
	parser = argparse.ArgumentParser()
	parser.add_argument(	'-c', '--classifier_name',
							metavar='O', type=str, nargs=1, dest='classifier_name', required=False,
							default='clf.pkl', help='path to output directory (local filesystem)', 
							action='store')
	args = parser.parse_args ()
	classifier_name = args.classifier_name[0]

	#=====[ TRAIN CLASSIFIER	]=====
	classifier = GestureClassifier(classifier_name=classifier_name)
	classifier.train()
	classifier.evaluate_self()
	classifier.save()
