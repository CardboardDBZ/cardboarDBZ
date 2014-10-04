import pickle
from PrimeSense import PrimeSense

if __name__ == '__main__':

	p = PrimeSense()
	p.pos_df = pickle.load(open('data/sample_pos_df.pkl'))
	df = p.pos_df
	origin, x_axis, y_axis, z_axis, H = p.coordinate_transform(df)
