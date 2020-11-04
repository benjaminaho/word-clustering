import json

# Get word to compare.
target = input("Type word to compare: ")

index = json.load(open("dictionary_inverse.json", "r"))

from word_trigrams import trigramize

# Find words which share the most bi and trigrams with target.
results = dict()
for gram in trigramize(target):
    if len(gram) == 1: # don't bother with monograms
        continue
    for word in index[gram]:
        if word not in results:
            results[word] = 1
        else:
            results[word] += 1

results = sorted(results.items(), key=lambda x: x[1], reverse=True)

json.dump(results, open("search_results/primitive/" + target + ".json", "w"))