import pickle
from PrimeSense import PrimeSense

if __name__ == '__main__':

	sample_video = pickle.load(open('./data/twoplayer_test_1.pkl','r'))
	p = PrimeSense(sample_video)



