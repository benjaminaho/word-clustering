"""Get and save the log likelihood ratio between every letter and its contiguous grams in a word.
"""

import json

prec_scores = json.load(open("collocations/preceding_gram_scores.json", "r"))
succ_scores = json.load(open("collocations/succeeding_gram_scores.json", "r"))

word = input("Type word to analyze: ")
word += " "

answer = [[0 for _ in range(len(word))] for _ in range(len(word))]

for i in range(len(word)):
    for j in range(len(word)):
        try:
            if i > j:
                answer[i][j] = prec_scores[word[j:i+1]]
            elif i < j:
                answer[i][j] = succ_scores[word[i:j+1]]
        except KeyError:
            print("this is a thing that happens")
            answer[i][j] = 0

json.dump(answer, open("collocations/analysis/" + word[:-1] + ".json", "w"), indent=4)