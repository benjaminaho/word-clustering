"""
"""

import json, math

gram_cnts = json.load(open("gram_cnts.json", "r"))

alphabet = set(" abcdefghijklmnopqrstuvwxyz.")

def smooth(val):
    if val == 1:
        return 0.999999
    elif val == 0:
        return 0.000001
    return val

def likelihoods(letter, prev="", post=""):

    whole_gram = prev + letter + post

    space = sum([gram_cnts[l] for l in alphabet - {" ", "."}])
    
    cnt_prev_post = sum([gram_cnts[prev+l+post] for l in alphabet if prev+l+post in gram_cnts])

    h0_prob = gram_cnts[letter] / space

    def likelihood(tt_prob, tf_prob, ft_prob, ff_prob):
        tt_prob = smooth(tt_prob)
        tf_prob = smooth(tf_prob)
        ft_prob = smooth(ft_prob)
        ff_prob = smooth(ff_prob)
        return -2 * (

            # log of the probability of the "prev comes before and post comes after"-class of the observations
            # letter | prev & post
            gram_cnts[whole_gram] * math.log(tt_prob) +
            # not letter | prev & post
            (cnt_prev_post - gram_cnts[whole_gram]) * math.log(1 - tt_prob) +

            # letter | prev & not post
            (gram_cnts[prev + letter] - gram_cnts[whole_gram]) * math.log(tf_prob) +
            # not letter | prev & not post
            (gram_cnts[prev] - gram_cnts[prev + letter]) * math.log(1 - tf_prob) +

            # letter | not prev & post
            (gram_cnts[letter + post] - gram_cnts[whole_gram]) * math.log(ft_prob) +
            # not letter | not prev & post
            (gram_cnts[post] - gram_cnts[letter + post]) * math.log(1 - ft_prob) +

            # letter | not prev & not post
            (gram_cnts[letter] - gram_cnts[prev + letter] - gram_cnts[letter + post] + gram_cnts[whole_gram]) * math.log(ff_prob) +
            # not letter | not prev & not post
            (space - gram_cnts[letter] - (cnt_prev_post - gram_cnts[whole_gram]) - (gram_cnts[prev] - gram_cnts[prev + letter]) - (gram_cnts[post] - gram_cnts[letter + post])) * math.log(1 - ff_prob)

        )
    
    h_prev_t = gram_cnts[prev + letter] / gram_cnts[prev]
    h_prev_f = (gram_cnts[letter] - gram_cnts[prev + letter]) / (space - gram_cnts[prev])
    h_post_t = gram_cnts[letter + post] / gram_cnts[post]
    h_post_f = (gram_cnts[letter] - gram_cnts[letter + post]) / (space - gram_cnts[post])
    h_prev_post_t = gram_cnts[whole_gram] / cnt_prev_post
    h_prev_post_f = (gram_cnts[letter] - gram_cnts[whole_gram]) / (space - cnt_prev_post)
    h_none_t = (gram_cnts[letter] - gram_cnts[prev + letter] - gram_cnts[letter + post] + gram_cnts[whole_gram]) / (space - gram_cnts[prev] - gram_cnts[post] + cnt_prev_post)
    h_none_f = (gram_cnts[prev + letter] + gram_cnts[letter + post] - gram_cnts[whole_gram]) / (gram_cnts[prev] + gram_cnts[post] - cnt_prev_post)

    L_h0 = likelihood(h0_prob, h0_prob, h0_prob, h0_prob)
    L_h_prev_post = likelihood(h_prev_post_t, h_prev_post_f, h_prev_post_f, h_prev_post_f)
    L_h_prev = likelihood(h_prev_t, h_prev_t, h_prev_f, h_prev_f)
    L_h_post = likelihood(h_post_t, h_post_f, h_post_t, h_post_f)
    L_h_none = likelihood(h_none_f, h_none_f, h_none_f, h_none_t)

    return L_h0, L_h_prev_post, L_h_prev, L_h_post, L_h_none
    

word = input("Type word to analyze: ")
word = " " + word + "."
theories = []
for i in range(1, len(word)-1):
    for j in range(0, i):
        for k in range(i+2, len(word)+1):
            L_h0, L_h_prev_post, L_h_prev, L_h_post, L_h_none = likelihoods(word[i], word[j:i], word[i+1:k])

            theories.append((L_h0-L_h_prev_post, j, k))
            theories.append((L_h0-L_h_prev, j, i+1))
            theories.append((L_h0-L_h_post, i, k))
            theories.append((L_h0-L_h_none, i, i+1))

theories = sorted(theories, key=lambda x: x[0], reverse=True)
seen = set()
collocs = []
theoryiter = iter(theories)
while len(seen) < len(word):
    try:
        _, alp, ome = next(theoryiter)
    except StopIteration:
        print("it's absolutely nuts that this is happening")
        break
    theory = set(range(alp, ome))
    tem = True
    for i in range(len(collocs)):
        if collocs[i].issubset(theory):
            if not tem:
                collocs[i] = None
                continue
            collocs[i] = theory
            tem = False
    if tem:
        collocs.append(theory)
    for idx in theory:
        seen.add(idx)
    while None in collocs:
        collocs.remove(None)

for i in range(len(collocs)):
    if collocs[i] is None:
        continue
    for j in range(i+1, len(collocs)):
        if collocs[j] is None:
            continue
        if (collocs[j]-{0,len(word)-1}).issubset(collocs[i]):
            collocs[j] = None
        elif (collocs[i]-{0,len(word)-1}).issubset(collocs[j]):
            collocs[i] = None
            break
while None in collocs:
        collocs.remove(None)

for colloc in [sorted(list(c)) for c in collocs]:
    print(word[colloc[0]:colloc[-1]+1])

#json.dump(sorted(anss, key=lambda x: max(x[4]), reverse=True), open("collocations/analysis/" + word[1:-1] + ".json", "w"), indent=4)
