import pickle
from DBZHost import DBZController

if __name__ == '__main__':

	dbz_controller = DBZController(debug=True, data_dir='../data')
	dbz_controller.record_gesture()
