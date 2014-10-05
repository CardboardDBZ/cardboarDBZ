from PrimeSense import PrimeSense 

if __name__ == '__main__':

	p = PrimeSense(debug=True)
	raw_frames = p.record()