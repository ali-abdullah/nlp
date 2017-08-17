from collections import Counter

class NaiveBayesText:

	'''
		This class has functions that :
		 train the model 
		 run it on text inputs and classifies them
		 checks for scores on given test X and y
		
		By default if no input is given it uses 
		 predefined lists

		for training
		X = [
		['words', 'inside', 'a', 'list'],
		['they', 'scored', 'four', 'goals']
		[....]
		] (Text)
		Y = ['words','sports', ....] (topics)
	'''

	words = [
		['this', 'chicken', 'tastes' , 'amazing'],
		['I', 'really', 'like', 'this', 'cake'],
		['this', 'chicken', 'is', 'horrible'],
		['I', 'hate' , 'the', 'cake']	
	]
	sentiment = ['positive', 'positive', 'negative' , 'negative']

	test = [
		['the', 'cake', 'is', 'amazing'], # 2 bad 1 both 1 good
		['really', 'chicken', 'tastes', 'horrible'] # 2 good 1 bad 1 both
	]

	test_y = ['positive','negative']

	def relative_frequency_counter(self, list_in):
		'''
		input : a list consisting of tokens
		output: a dictionary with keys equal to unique tokens and
			value equal to their frequency  
		''' 
		total_length = len(list_in)
		rf_dict = dict(Counter(list_in))
		for key in rf_dict.keys():
			rf_dict[key] = float(rf_dict[key]) / float(total_length)
		return rf_dict

	def init_nb_dict(self): 
		self.nb_dict = {} 
		for label in self.labels: 
			self.nb_dict[label] = {} 

	def max_class_rank(self, class_rankings):
		class_chance = 0
		class_prediction = 'nothing'
		for category in class_rankings.keys():
			if (class_rankings[category] > class_chance):
				class_prediction = category
				class_chance = class_rankings[category]
		return class_prediction

	def train(self, X = words, y = sentiment):

		self.labels = set(y)

		self.class_probability = self.relative_frequency_counter(y)
		
		self.init_nb_dict() # initializes nb_dict

		# final result for nb_dict:
		# nb_dict = {'positive':{'this': 1, 'is': 1 , ...} , 'negative':{'this': 1, 'will': 1, ...}}

		for category in self.nb_dict.keys():
			self.word_list =  []
			for counter in range(0,len(X)):
				if(y[counter] == category):
					self.word_list += X[counter]
			self.nb_dict[category] = self.relative_frequency_counter(self.word_list)
	
	def classify(self, X = test):
		# The user will pass in a single array or a list of arrays,
		# we shall then output the prediction as a list

		predictions = []
		for text in X:
			class_rankings = {}
			for category in self.nb_dict.keys():
				class_rank = self.class_probability[category]
				for word in text:
					if word in self.nb_dict[category].keys():
						class_rank *= self.nb_dict[category][word]
					else:
						class_rank *= 1
				class_rankings[category] = class_rank
			print(text)
			print("the class_ranking is: ")
			print(class_rankings) 
			class_prediction = self.max_class_rank(class_rankings)
			print("the class_prediction is: ")
			print(class_prediction)
			predictions.append(class_prediction)
		return predictions

	def score(self, X = test, y = test_y):
		results = self.classify(X)
		correct_predictions = 0
		incorrect_predictions = 0
		for i in range(0, len(y)):
			if results[i] == y[i]:
				correct_predictions += 1
			else:
				incorrect_predictions += 1
		score = correct_predictions / float(correct_predictions + incorrect_predictions)

		return score 