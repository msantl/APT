#!usr/bin/python

# n - n-gram
# inputFile - file iz kojeg cita 
# npr: za n=1 prebroji koliko puta se koja rijec pojavljuje
# vraca dict s elementima tuple: int, gdje je tuple
# n-gram(npr, (ja, sam)), a int je broj ponavljanja tog n-grama
# kod n = 1 tuplovi su oblika (rijec,)
def count_n_grams(n, inputFile):
	ngrams = {}

	for line in inputFile:
		line = line.strip()
		words = line.split()
		for i in range (0, len(words) - n + 1):
			ngram_list = []
			for j in range(0, n):
				ngram_list.append(words[i+j])
			ngram_tuple = tuple(ngram_list)
			if ngrams.has_key(ngram_tuple):
				ngrams[ngram_tuple] += 1
			else:
				ngrams[ngram_tuple] = 1
	
	inputFile.seek(0)
	return ngrams
	
