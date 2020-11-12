import json
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds

dictionary = json.load(open("dictionary.json", "r"))

# Assign each gram an index.
gram_idxs = dict()
cnt = 0
for word in dictionary:
    for gram in dictionary[word]:
        if gram not in gram_idxs:
            gram_idxs[gram] = cnt
            cnt += 1

# Build A matrix while assigning each word an index.
raw_A = []
word_idxs = dict()
for word in dictionary:
    vect = [0] * len(gram_idxs)
    for gram in dictionary[word]:
        vect[gram_idxs[gram]] += 1
    raw_A.append(vect)
    word_idxs[word] = len(raw_A) - 1
A = csc_matrix(raw_A, dtype=float).transpose()

# Save gram and word references to file.
json.dump(gram_idxs, open("lsi/gram_idxs.json", "w"))
json.dump(word_idxs, open("lsi/word_idxs.json", "w"))

# Calculate U, S, and Vt matrices.
u, s, vt = svds(A, k=100)

# Save matrices to file.
import numpy
numpy.save(open("lsi/u_mat.txt", 'wb'), u)
numpy.save(open("lsi/s_mat.txt", 'wb'), s)
numpy.save(open("lsi/vt_mat.txt", 'wb'), vt)