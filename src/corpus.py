from collections import Counter
from collections import defaultdict
from sets import Set
import abc

class Corpus:

    DEFAULT_PROB = 0.0
    BOS = "<s>"
    EOS = "</s>"

    def __init__(self, max_n):
        self.max_n = max_n
        self.total_number_of_words = 0

        # how many ngrams there is in corpus
        self.n_gram_map = {}
        # map ngram to word count
        self.n_gram_word_count_map = {}
        # countinuation counts
        self.continuation_map = {}

        for i in range(self.max_n):
            n = i + 1
            self.n_gram_word_count_map[n] = defaultdict(Counter)
            self.continuation_map[n] = defaultdict(set)
            self.n_gram_map[n] = set()

    def get_ngram_count(self, n, ngram, word):
        return self.n_gram_word_count_map[n][ngram][word]

    def get_unique_words(self):
        return self.n_gram_map[1]

    def get_total_number_of_words(self):
        return self.total_number_of_words

    def get_prefix_count(self, n, ngram):
        return sum(self.n_gram_word_count_map[n][ngram].values())

    def get_next_word(self, ngram):
        probabilities = []
        words = self.get_unique_words()

        for word in words:
            # because words are tuples
            word = word[0]
            prob = self.get_word_probability(ngram, word)
            probabilities.append((word, prob))

        max_prob = probabilities[0][1]
        predicted_word = probabilities[0][0]
        for i in probabilities:
            if i[1] > max_prob:
                max_prob = i[1]
                predicted_word = i[0]

        return predicted_word

    @abc.abstractmethod
    def get_word_probability(self, ngram, word):
        pass

    def train(self, input_file, discount=0.75):
        self.discount = discount

        for sentence in input_file:
            # sentence format is "<s> word ... word </s>"
            words = sentence.split()
            self.total_number_of_words += len(words)

            for i in range(self.max_n):
                n = i + 1
                ngram = (self.BOS, ) * (n - 1)

                for word in words:
                    self.n_gram_word_count_map[n][ngram][word] += 1
                    self.n_gram_map[n].add(ngram + (word, ))
                    self.continuation_map[n][word].add(ngram)

                    if len(ngram) > 0:
                        ngram = ngram[1:] + (word,)


