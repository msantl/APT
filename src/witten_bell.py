#!usr/bin/python

from __future__ import division
from corpus import *

class Witten_Bell(Corpus):
    def get_word_probability(self, ngram, word):
        n = len(ngram) + 1

        c_up = self.get_ngram_count(n, ngram, word)

        c_down = self.get_ngram_count(n - 1, ngram[1:], word)

        n_plus = self.get_prefix_count(n, ngram)

        if c_down + n_plus == 0:
            p = self.DEFAULT_PROB
        elif len(ngram) == 1:
            p = (c_up + n_plus * self.get_ngram_count(1, (), word) / self.get_total_number_of_words()) / (c_down + n_plus)
        else:
            p = (c_up + n_plus * self.get_word_probability(ngram[1:], word)) / (c_down + n_plus)

        return p

