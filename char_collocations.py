"""
"""
import time
t_prev_post = 0
t_prev = 0
t_post = 0
t_gram = 0

import json, math, gram_tree

cnts = gram_tree.Counts(" abcdefghijklmnopqrstuvwxyz.", json.load(open("gram_cnts.json", "r")))

def smooth(val):
    if val == 1:
        return 0.999999
    elif val == 0:
        return 0.000001
    return val

def likelihoods(prev, gram, post):

    space = cnts.by_len(len(gram))

    global t_gram, t_prev, t_post, t_prev_post

    t = time.time()

    cnt_gram = cnts.gram(gram)
    cnt_whole = cnts.gram(prev + gram + post)
    cnt_prev_gram = cnts.gram(prev + gram)
    cnt_gram_post = cnts.gram(gram + post)
    t_gram += time.time()-t
    t = time.time()

    cnt_prev_post = cnts.prev_post(prev, len(gram), post)
    t_prev_post += time.time()-t
    t = time.time()

    cnt_prev = cnts.prev(prev, len(gram))
    t_prev += time.time()-t
    t = time.time()
    
    cnt_post = cnts.post(len(gram), post)
    t_post += time.time()-t
    #t = time.time()

    def likelihood(tt_prob, tf_prob, ft_prob, ff_prob):
        tt_prob = smooth(tt_prob)
        tf_prob = smooth(tf_prob)
        ft_prob = smooth(ft_prob)
        ff_prob = smooth(ff_prob)
        return -2 * (

            # log of the probability of the "prev comes before and post comes after"-class of the observations
            # gram | prev & post
            cnt_whole * math.log(tt_prob) +
            # not gram | prev & post
            (cnt_prev_post - cnt_whole) * math.log(1 - tt_prob) +

            # gram | prev & not post
            (cnt_prev_gram - cnt_whole) * math.log(tf_prob) +
            # not gram | prev & not post
            (cnt_prev - cnt_prev_gram) * math.log(1 - tf_prob) +

            # gram | not prev & post
            (cnt_gram_post - cnt_whole) * math.log(ft_prob) +
            # not gram | not prev & post
            (cnt_post - cnt_gram_post) * math.log(1 - ft_prob) +

            # gram | not prev & not post
            (cnt_gram - cnt_prev_gram - cnt_gram_post + cnt_whole) * math.log(ff_prob) +
            # not gram | not prev & not post
            (space - cnt_gram - (cnt_prev_post - cnt_whole) - (cnt_prev - cnt_prev_gram) - (cnt_post - cnt_gram_post)) * math.log(1 - ff_prob)

        )

    h0_prob = cnt_gram / space
    
    h_prev_t = cnt_prev_gram / cnt_prev
    h_prev_f = (cnt_gram - cnt_prev_gram) / (space - cnt_prev)
    h_post_t = cnt_gram_post / cnt_post
    h_post_f = (cnt_gram - cnt_gram_post) / (space - cnt_post)
    h_prev_post_t = cnt_whole / cnt_prev_post
    h_prev_post_f = (cnt_gram - cnt_whole) / (space - cnt_prev_post)
    h_none_t = (cnt_gram - cnt_prev_gram - cnt_gram_post + cnt_whole) / (space - cnt_prev - cnt_post + cnt_prev_post)
    h_none_f = (cnt_prev_gram + cnt_gram_post - cnt_whole) / (cnt_prev + cnt_post - cnt_prev_post)

    t = time.time()

    L_h0 = likelihood(h0_prob, h0_prob, h0_prob, h0_prob)
    L_h_prev_post = likelihood(h_prev_post_t, h_prev_post_f, h_prev_post_f, h_prev_post_f)
    L_h_prev = likelihood(h_prev_t, h_prev_t, h_prev_f, h_prev_f)
    L_h_post = likelihood(h_post_t, h_post_f, h_post_t, h_post_f)
    L_h_none = likelihood(h_none_f, h_none_f, h_none_f, h_none_t)

    return L_h0, L_h_prev_post, L_h_prev, L_h_post, L_h_none
    
word = input("Type word to analyze: ")
while word != "stopnow":
    word = " " + word + "."
    theories = []
    #t = time.time()
    for i in range(1, len(word)-1):
        for j in range(i, len(word)-1):

            for k in range(0, i):
                for l in range(j+1, len(word)):
                    t = time.time()
                    L_h0, L_h_prev_post, L_h_prev, L_h_post, L_h_none = likelihoods(word[k:i], word[i:j+1], word[j+1:l+1])
                    print(k,i,j,l, time.time()-t)
                    theories.append((L_h0-L_h_prev_post, k, l))
                    theories.append((L_h0-L_h_prev, k, j))
                    theories.append((L_h0-L_h_post, i, l))
                    theories.append((L_h0-L_h_none, i, j))

    print(t_gram, t_prev, t_post, t_prev_post)
    #print(sorted(list(cnts.rec.items()), key=lambda x: x[1]))
    #print(cnts.rec2)
    t_gram=t_prev=t_post=t_prev_post = 0

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
        theory = set(range(alp, ome+1))
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

    word = input("Type word to analyze: ")

    json.dump(sorted(theories, key=lambda x: x[0], reverse=True), open("collocations/analysis/" + word[1:-1] + ".json", "w"), indent=4)
