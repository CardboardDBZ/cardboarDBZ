import pickle
from DBZHost import DBZController


if __name__ == '__main__':

	controller = DBZController(num_players=1, data_dir='../data')
	while True:
		controller.update_game()


