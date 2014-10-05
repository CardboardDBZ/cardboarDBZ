from DBZHost import DBZController

if __name__ == '__main__':

	dbz_controller = DBZController(debug=True)
	raw_frames = dbz_controller.record()

