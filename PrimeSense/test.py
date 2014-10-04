import pickle
from PrimeSense import PrimeSense

if __name__ == '__main__':

	p = PrimeSense()
	p.pos_df = pickle.load(open('data/sample_pos_df.pkl'))
	df = p.pos_df
	Hc = p.to_human_coords(df)