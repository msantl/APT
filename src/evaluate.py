from corpus import *
from witten_bell import *
from kneser_ney import *

import sys
import math
import codecs

def get_number_of_words_in_file(filename):
    f_handle = open(evaluate)
    cnt = 0

    for line in f_handle.readlines():
        cnt += len(line.split()[1:-1])

    f_handle.close()
    return cnt


def calculate(smooth, ngram, train_set, eval_set):
    P = 1.0
    H = 0.0
    PP = 0.0

    n = ngram - 1

    f_handle = open(train_set)
    smooth.train(f_handle)
    f_handle.close()

    Wt = get_number_of_words_in_file(eval_set)

    f_handle = open(eval_set)

    probabilities = list()

    for sentence in f_handle.readlines():
        sentence_probability = 1.0

        sentence = sentence.split()[1:-1]

        if len(sentence) < ngram: continue

        for i in range(len(sentence) - n):
            context = tuple(sentence[i:i + n])
            word = sentence[i + n]

            word_probability = smooth.get_word_probability(context, word)
            sentence_probability *= word_probability

            # print context, word, word_probability

        probabilities.append(sentence_probability)

        # print sentence, sentence_probability

    f_handle.close()

    total = sum(probabilities)

    for p in probabilities:
        if (p / total) > 0.0:
            P *= p

    H = -1.0 / Wt * math.log(P, 2)
    PP = 2 ** H

    print "\tVjerojatnost = ", P
    print "\tEntropija = ", H
    print "\tPerpleksija = ", PP


training = sys.argv[1] # "../common/corpus_t.txt"
evaluate = sys.argv[2] # "../common/corpus_e.txt"

print "Training corpus: ", training
print "Evaluating on  : ", evaluate

print "Kneser Ney, n = 2"
calculate(KneserNey(4), 2, training, evaluate)

print "Witten Bell, n = 2"
calculate(Witten_Bell(4), 2, training, evaluate)

print "Kneser Ney, n = 3"
calculate(KneserNey(4), 3, training, evaluate)

print "Witten Bell, n = 3"
calculate(Witten_Bell(4), 3, training, evaluate)

print "Kneser Ney, n = 4"
calculate(KneserNey(4), 4, training, evaluate)

print "Witten Bell, n = 4"
calculate(Witten_Bell(4), 4, training, evaluate)

