#!usr/bin/python

from __future__ import division
from sys import argv
from n_gram_counter import *

#inputPath = argv[1]
#inputFile = open(inputPath, 'r')

def n_plus_counter(sequence, inputFile):
	result = []
	sequence_length = len(sequence)
	for line in inputFile:
		line = line.strip()
		words = line.split()
		for i in range (0, len(words) - sequence_length):
			ngram_list = []
			for j in range(0, sequence_length):
				ngram_list.append(words[i+j])
			ngram_tuple = tuple(ngram_list)
			if ngram_tuple == sequence:
				result.append(words[i+sequence_length])
	
	inputFile.seek(0)
	result = list(set(result))
	return len(result)

def witten_bell(n, total_number_of_words, test_sequence, next_word):
	whole_sequence = list(test_sequence)
	whole_sequence.append(next_word)
	whole_sequence = tuple(whole_sequence) 
	
	n_gram = count_n_grams(n, inputFile)
	n_minus_one_gram = count_n_grams(n-1, inputFile)
	
	c_up = 0
	if n_gram.has_key(whole_sequence):
		c_up = n_gram[whole_sequence]
	
	
	c_down = 0
	if n_minus_one_gram.has_key(test_sequence):
		c_down = n_minus_one_gram[test_sequence]
		
	n_plus = n_plus_counter(test_sequence, inputFile)
	
	test_sequence = list(test_sequence)
	test_sequence.pop(0)
	test_sequence = tuple(test_sequence)
	
	if len(test_sequence) == 1:
		uni_words = count_n_grams(1, inputFile)
		p = (c_up + n_plus * uni_words[(next_word, )] / total_number_of_words) / (c_down + n_plus)
		return p
		
	p = (c_up + n_plus * witten_bell(n-1, total_number_of_words, test_sequence, next_word)) / (c_down + n_plus)
	
	return p
	
#n = 3
#test_sequence = ('Administration', 'of')

#unique_words = count_n_grams(1, inputFile)

#total_number_of_words = 0
#for key in unique_words:
	#total_number_of_words += unique_words[key]

#probabilities = []
#for word, number in unique_words.iteritems():
	#prob = witten_bell(3, total_number_of_words, test_sequence, word[0])
	#probabilities.append((word[0], prob))

#max_prob = probabilities[0][1]
#predicted_word = probabilities[0][0]
#for i in probabilities:
	#if i[1] > max_prob:
		#max_prob = i[1]
		#predicted_word = i[0]
	
#print "Predicted word: " + predicted_word
