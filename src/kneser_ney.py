#!usr/bin/python

from __future__ import division
from corpus import *

class KneserNey(Corpus):
    def get_word_probability(self, ngram, word):
        n = len(ngram) + 1

        if n == 1:
            return float(len(self.continuation_map[2][word])) / len(self.n_gram_map[2])

        c_total = self.get_prefix_count(n, ngram)
        previous_prob = self.get_word_probability(ngram[1:], word)

        if c_total == 0:
            return previous_prob

        c = self.get_ngram_count(n, ngram, word)
        c_star = max(c - self.discount, 0)

        # N1 = number of different words Wi-1 that preceed Wi
        N1 = len([v for v in self.n_gram_word_count_map[n][ngram].values() if v > 0])

        return float(c_star + self.discount * N1 * previous_prob) / c_total

