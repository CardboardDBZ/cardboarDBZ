import pickle
from PrimeSense import PrimeSense

if __name__ == '__main__':

	sample_frame = pickle.load(open('./data/raw_frame_sample.pkl','r'))
	p = PrimeSense()
	p.update(input_frame=sample_frame)

	s1_c = p.skeleton_poses_c[0]
	s1_h = p.to_human_coords(s1_c)

