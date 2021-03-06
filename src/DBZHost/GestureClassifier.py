import os
import pickle
import numpy as np
import pandas as pd
import sklearn 
from sklearn import cross_validation
from sklearn.svm import SVC, NuSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA, SparsePCA, DictionaryLearning
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt

class GestureClassifier:

	GESTURE_CONFIDENCE_THRESHOLD = 0.9

	def __init__(self, data_dir=os.path.join(os.getcwd(), 'data'), classifier_name='clf.pkl'):
		self.data_dir = data_dir
		self.gestures_dir = os.path.join(self.data_dir, 'gestures')
		self.classifiers_dir = os.path.join(self.data_dir, 'classifiers')
		self.classifier_path = os.path.join(self.classifiers_dir, classifier_name)

		self.data_loaded = False
		self.classifier_loaded = False

	################################################################################
	####################[ LOADING/FORMATTING DATA ]#################################
	################################################################################

	def featurize(self, gesture_df):
		"""
			given a gesture represented as a dataframe, this will return a numpy 
			array as a feature vector
		"""
		gesture_df = gesture_df.copy()

		#=====[ Experiment: relative positions	]=====
		gesture_df['hands_avg'] = (gesture_df['right_hand'] + gesture_df['left_hand'])/2.
		gesture_df['elbows_avg'] = (gesture_df['right_elbow'] + gesture_df['left_elbow'])/2.
		gesture_df['hands_diff'] = np.abs(gesture_df['right_hand'] - gesture_df['left_hand'])

		return np.array(gesture_df).flatten()


	def load_gesture_data(self, gesture_name):
		"""
			returns c_dfs, h_dfs
			each is a list of dataframes representing the body in body, human
			coordinates
		"""
		gesture_dir = self.gesture_directories[gesture_name]
		dicts = [pickle.load(open(os.path.join(gesture_dir, fn))) for fn in os.listdir(gesture_dir)]
		c_dfs = [d['c_coords'] for d in dicts]
		h_dfs = [d['h_coords'] for d in dicts]
		return c_dfs, h_dfs


	def get_X_y(self):
		"""
			goes from self.data -> featurized X and y matrices for prediction 
		"""
		Xs, ys = [], []
		for name, dfs_dict in self.data.items():
			h_dfs = dfs_dict['h_coords']
			data = np.matrix([self.featurize(df) for df in h_dfs])
			Xs.append(data)
			ys.append(np.array([name]*data.shape[0]))
		self.X = np.concatenate(Xs)
		self.y = np.concatenate(ys)
		return self.X, self.y


	def load_data(self):
		"""
			sets self.data to a dict mapping as follows:
				self.data: gesture_name -> numpy matrix
			also sets self.X, self.y for training and whatnot
		"""
		if not self.data_loaded:
			self.gesture_names = os.listdir(self.gestures_dir)
			self.gesture_directories = {name:os.path.join(self.gestures_dir, name) for name in os.listdir(self.gestures_dir)}
			self.data = {}
			for name in self.gesture_names:
				c_dfs, h_dfs = self.load_gesture_data(name)
				self.data[name] = {'c_coords':c_dfs, 'h_coords':h_dfs}
			self.X, self.y = self.get_X_y ()
			self.data_loaded = True


	def load_classifier(self):
		"""
			loads self.classifier 
		"""
		if not self.classifier_loaded:
			self.classifier = pickle.load(open(self.classifier_path, 'r'))
			self.classifier_loaded = True





	################################################################################
	####################[ TRAINING/PREDICTION ]#####################################
	################################################################################

	def train(self):
		"""
			trains classifier based on all data available
		"""
		self.load_data()
		self.classifier = KNeighborsClassifier(n_neighbors=2)
		# self.classifier = LogisticRegression()
		self.classifier.fit(self.X, self.y)
		self.classifier_loaded = True


	def predict(self, gesture_df):
		"""
			returns a prediction based on the pose 
		"""
		assert self.classifier_loaded
		prob_predicitons = self.classifier.predict_proba(self.featurize(gesture_df))
		if not np.max(prob_predicitons) > self.GESTURE_CONFIDENCE_THRESHOLD:
			return ['no_gesture']
		else:
			return self.classifier.predict(self.featurize(gesture_df))


	def save(self):
		"""
			saves the current classifier 
		"""
		pickle.dump(self.classifier, open(self.classifier_path, 'w'))





	################################################################################
	####################[ EVALUATION/CROSSVALIDATION ]##############################
	################################################################################

	def evaluate_models(self):
		"""
			evaluates the model 
		"""
		#=====[ Step 1: Get X, y	]=====
		self.load_data()
		X, y = self.X, self.y

		clf_log = LogisticRegression()
		clf_knn = KNeighborsClassifier(n_neighbors=5)
		clf_nb = MultinomialNB()

		#=====[ Step 2: Cross Validation	]=====
		print '===[ RAW DATA ]==='
		scores_log = cross_validation.cross_val_score(clf_log, X, y)
		scores_knn = cross_validation.cross_val_score(clf_knn, X, y)
		print 'LOG: ', scores_log
		print 'KNN: ', scores_knn

		


		######[ DIMENSIONALITY REDUCTION: PCA	]#####
		print '===[ With PCA ]==='
		X_PCA = PCA(n_components=10).fit_transform(X)
		scores_log = cross_validation.cross_val_score(clf_log, X_PCA, y)
		scores_knn = cross_validation.cross_val_score(clf_knn, X_PCA, y)
		print 'LOG: ', scores_log
		print 'KNN: ', scores_knn

		# print '===[ With Dictionary Learning ]==='
		# X_DL = DictionaryLearning(n_components=10).fit_transform(X)
		# scores_log = cross_validation.cross_val_score(clf_log, X_DL, y)
		# scores_knn = cross_validation.cross_val_score(clf_knn, X_DL, y)
		# scores_nb = cross_validation.cross_val_score(clf_nb, X_DL, y)
		# print 'LOG: ', scores_log
		# print 'KNN: ', scores_knn
		# print 'NB: ', scores_nb


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


	def evaluate_self(self):
		"""
			evaluates only the currently loaded classifier 
		"""
		assert self.classifier_loaded
		scores = cross_validation.cross_val_score(self.classifier, self.X, self.y)
		print "CROSS VALIDATION SCORES:"
		print scores



if __name__ == '__main__':

	classifier = GestureClassifier()
	classifier.evaluate_models()


