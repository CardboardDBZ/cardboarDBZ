import os
import pickle
import numpy as np
import pandas as pd
import sklearn 
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

class GestureClassifier:

	def __init__(self, data_dir=os.path.join(os.getcwd(), 'data/gestures')):
		self.data_dir = data_dir
		self.load_data()

	################################################################################
	####################[ LOADING/FORMATTING DATA ]#################################
	################################################################################

	def load_data(self):
		"""
			sets self.data to a dict mapping as follows:
				self.data: gesture_name -> numpy matrix
		"""
		self.gesture_names = os.listdir(self.data_dir)
		self.gesture_directories = {name:os.path.join(self.data_dir, name) for name in os.listdir(self.data_dir)}
		self.data = {}
		for name in self.gesture_names:
			self.data[name] = self.load_gesture_data(name)


	def featurize(self, gesture_df):
		"""
			given a gesture represented as a dataframe, this will return a numpy 
			array as a feature vector
		"""
		return np.array(gesture_df).flatten()


	def load_gesture_data(self, gesture_name):
		"""
			given a gesture name, this will return a numpy matrix where rows 
			are the gestures
		"""
		gesture_dir = self.gesture_directories[gesture_name]
		dfs = [pickle.load(open(os.path.join(gesture_dir, fn))) for fn in os.listdir(gesture_dir)]
		return np.matrix([self.featurize(df) for df in dfs])


	def get_X_y(self):
		"""
			goes from self.data -> X and y matrices for prediction 
		"""
		Xs, ys = [], []
		for name, data in self.data.items():
			Xs.append(data)
			ys.append(np.array([name]*data.shape[0]))
		self.X = np.concatenate(Xs)
		self.y = np.concatenate(ys)
		return self.X, self.y






	################################################################################
	####################[ TRAINING/CROSSVALIDATION ]################################
	################################################################################

	def evaluate_models(self):
		"""
			evaluates the model 
		"""
		#=====[ Step 1: Get X, y	]=====
		X, y = self.get_X_y()

		#=====[ Step 2: Cross Validation	]=====
		clf_svm = SVC(kernel='linear', C=1)
		clf_log = LogisticRegression()
		clf_knn = KNeighborsClassifier(n_neighbors=5)
		scores_svm = cross_validation.cross_val_score(clf_svm, X, y)
		scores_log = cross_validation.cross_val_score(clf_log, X, y)
		scores_knn = cross_validation.cross_val_score(clf_knn, X, y)
		print 'SVM: ', scores_svm
		print 'LOG: ', scores_log
		print 'KNN: ', scores_knn

		#=====[ Step 3: check out confusion matrix	]=====
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.4, random_state=0)
		y_pred = clf_log.fit(X_train, y_train).predict(X_test)
		cm = confusion_matrix(y_test, y_pred)
		plt.matshow(cm)
		plt.title('Confusion matrix')
		plt.colorbar()
		plt.ylabel('True label')
		plt.xlabel('Predicted label')
		plt.show()





if __name__ == '__main__':

	classifier = GestureClassifier()
	classifier.evaluate_models()


