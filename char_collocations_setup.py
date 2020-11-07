"""
Create dictionary of gram : [[a gram which follows gram in a word, number of words in which this gram follows gram] for each gram which follows gram] key-value pairs.

This program effectively finds all 3-, 4-, 5-, and 6-grams in the corpus, indexed by their primary
bigram in the former two, and their primary trigram in the latter. Each pair (bigram-monogram,
bigram-bigram, trigram-bigram, or trigram-trigram) is a possible "collocation," which is determined
in a subsequent program.
"""

import json

word_index = json.load(open("dictionary.json", "r"))
gram_index = json.load(open("dictionary_inverse.json", "r"))

following_grams = dict()

for gram in gram_index:
    next_grams = dict()
    if len(gram) == 1:
        continue
    if len(gram) == 2:
        for word in gram_index[gram]:
            idx = word_index[word].index(gram)
            if idx < len(word) * 3 - 4: # three-char strings
                nxg = word_index[word][int((idx-len(word))/2)+1]
                if nxg not in next_grams:
                    next_grams[nxg] = 1
                else:
                    next_grams[nxg] += 1
            if idx < len(word) * 3 - 6: # four-char strings
                nxg = word_index[word][idx+4]
                if nxg not in next_grams:
                    next_grams[nxg] = 1
                else:
                    next_grams[nxg] += 1
    elif len(gram) == 3:
        for word in gram_index[gram]:
            idx = word_index[word].index(gram)
            if idx < len(word) * 3 - 7: # five-char strings
                nxg = word_index[word][idx+5]
                if nxg not in next_grams:
                    next_grams[nxg] = 1
                else:
                    next_grams[nxg] += 1
            if idx < len(word) * 3 - 9: # six-char strings
                nxg = word_index[word][idx+6]
                if nxg not in next_grams:
                    next_grams[nxg] = 1
                else:
                    next_grams[nxg] += 1
    following_grams[gram] = sorted(next_grams.items(), key=lambda x: x[1], reverse=True)

json.dump(following_grams, open("following_grams.json", "w"))