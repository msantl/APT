from sets import Set
import abc

class Corpus:
	def __init__(self):
		# self.max_n
		# self.n_gram_map = {}
		self.n_gram_counts = {}
		self.n_gram_after_word_count = {} # genious name xD # how many different words can be find after ngram
		# self.corpus
		self.unique_words = []
		# self.number_of_unique_words
		self.total_number_of_words = 0
		
	def get_ngrams_counts(self):
		return self.n_gram_counts
	
	def get_unique_words(self):
		return self.unique_words
	
	def get_n_gram_after_word_count(self):
		return self.n_gram_after_word_count

	def get_total_number_of_words(self):
		return self.total_number_of_words

	def get_next_word(self, ngram):
		probabilities = []
		for word in self.unique_words:
			prob = self.get_word_probability(ngram, word)
			probabilities.append((word, prob))

		max_prob = probabilities[0][1]
		predicted_word = probabilities[0][0]
		for i in probabilities:
			if i[1] > max_prob:
				max_prob = i[1]
				predicted_word = i[0]
		
		print predicted_word	
		#return predicted_word
	
	@abc.abstractmethod
	def get_word_probability(self, ngram, word):
		return
	
	def train(self, input_file, max_n, discount=0.75):
		self.max_n = max_n + 1 # + 1 because I need (n+1)-grams
		
		# n_gram_counts
		for n in range(1, max_n+1):
			for line in input_file:
				words = line.split()
				
				for i in range (0, len(words) - n + 1):
					ngram_list = []
					for j in range(0, n):
						ngram_list.append(words[i+j])
					# unique words
					if n == 1:
						self.total_number_of_words += 1
						self.unique_words.append(ngram_list[0])
					ngram_tuple = tuple(ngram_list)
					if self.n_gram_counts.has_key(ngram_tuple):
						self.n_gram_counts[ngram_tuple] += 1
					else:
						self.n_gram_counts[ngram_tuple] = 1

		

			input_file.seek(0)
		self.unique_words = list(Set(self.unique_words))
		
		# ovo predugo dela, treba nekaj drugo smisliti
		# n_gram_after_word_count
		for ngram in self.n_gram_counts:
			n_set = Set()
			for word in self.unique_words:
				new_ngram = list(ngram)
				new_ngram.append(word)
				new_ngram = tuple(new_ngram)
				if self.n_gram_counts.has_key(new_ngram):
					n_set.add(word)
			if len(n_set) != 0:
				self.n_gram_after_word_count[ngram] = len(n_set)
