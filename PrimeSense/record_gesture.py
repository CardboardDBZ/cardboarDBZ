import pickle
from PrimeSense import PrimeSense

if __name__ == '__main__':

	p = PrimeSense(record=True)
	print "HERE"
	p.record_gesture()
