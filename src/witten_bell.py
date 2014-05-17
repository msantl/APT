#!usr/bin/python

from __future__ import division
from corpus import *

class Witten_Bell(Corpus):
	def get_word_probability(self, ngram, word):
		whole_sequence = list(ngram)
		whole_sequence.append(word)
		whole_sequence = tuple(whole_sequence) 
		
		n_gram_counts = Corpus.get_ngrams_counts(self)
		n_gram_after_word_count = Corpus.get_n_gram_after_word_count(self)
		unique_words = Corpus.get_unique_words(self)
		
		c_up = 0
		if n_gram_counts.has_key(whole_sequence):
			c_up = n_gram_counts[whole_sequence]
		
		
		c_down = 0
		if n_gram_counts.has_key(ngram):
			c_down = n_gram_counts[ngram]
		
		n_plus = 0
		if n_gram_after_word_count.has_key(ngram):
			n_plus = n_gram_after_word_count[ngram]
		
		ngram = list(ngram)
		ngram.pop(0)
		ngram = tuple(ngram)
		
		if len(ngram) == 1:
			if c_down+n_plus == 0:
				return 0
			p = (c_up + n_plus * n_gram_counts[(word, )] / Corpus.get_total_number_of_words(self)) / (c_down + n_plus)
			return p
			
		p = (c_up + n_plus * get_word_probability(self, ngram, word)) / (c_down + n_plus)
		
		return p

