import numpy, json

# Get word to compare.
target = input("Type word to compare: ")

# Load SVD matrices.
s = numpy.load(open("lsi/s_mat.txt", "rb"))
u = numpy.load(open("lsi/u_mat.txt", "rb"))

# Load gram and word index references.
gram_idxs = json.load(open("lsi/gram_idxs.json", "r"))
word_idxs = json.load(open("lsi/word_idxs.json", "r"))

from word_trigrams import trigramize

# Create vector representation of target word.
raw_target_vect = [0] * len(gram_idxs)
for gram in trigramize(target):
    if gram in gram_idxs:
        raw_target_vect[gram_idxs[gram]] = 1
    else:
        print("\"" + gram + "\" unseen in data")
target_vect = numpy.array(raw_target_vect).dot(u)
target_vect /= numpy.linalg.norm(target_vect)

# Calculate similarity score for each word in the dictionary wrt the target.
vt = numpy.load(open("lsi/vt_mat.txt", "rb"))
scores = target_vect.dot(vt)
v = numpy.diag(s).dot(vt).transpose()
for word_idx in range(len(v)):
    scores[word_idx] /= numpy.linalg.norm(v[word_idx])

# Match scores with respective words.
word_scores = dict()
for word in word_idxs:
    word_scores[word] = scores[word_idxs[word]]

# Write words sorted by score to file.
word_scores = [y[0] for y in sorted(word_scores.items(), key=lambda x: x[1], reverse=True)]
json.dump(word_scores, open("search_results/lsi" + target + ".json", "w"))