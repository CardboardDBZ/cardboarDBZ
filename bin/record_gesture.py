import pickle
from DBZHost import DBZController

if __name__ == '__main__':

	dbz_controller = DBZController(debug=True)
	dbz_controller.record_gesture()
