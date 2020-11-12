"""For every gram+letter or letter+gram in the corpus, determine the log likelihood ratio of the observations under the hypotheses of independence between occurences of gram and letter and of dependence.
"""

import json, math

gram_cnts = json.load(open("gram_cnts.json", "r"))
lett_cnts_by_gram_lens = json.load(open("num_gram_lens.json", "r"))

alphabet = "abcdefghijklmnopqrstuvwxyz "

gram_len_cnts = [0 for _ in range(31)] #[sum([gram_cnts[m] for m in alphabet])] 
for i in range(1, len(gram_len_cnts)):
    for let in lett_cnts_by_gram_lens[0]:
        gram_len_cnts[i] += lett_cnts_by_gram_lens[0][let][i-1]
#json.dump(gram_len_cnts, open("gram_len_cnts.json", "w"))

def log_lam(direction, gram, lett):
    if (gram_len_cnts[len(gram)] - gram_cnts[gram][direction]) == 0:
        print(gram + lett)
        return 0

    cnt_lett = lett_cnts_by_gram_lens[direction][lett][len(gram)-1]
    cnt_gram = gram_cnts[gram][direction]
    cnt_both = gram_cnts[gram + lett][direction] if direction == 0 else gram_cnts[lett + gram][direction]

    h0_prob = cnt_lett / gram_len_cnts[len(gram)]
    h1_prob_t = cnt_both / cnt_gram
    h1_prob_f = (cnt_lett - cnt_both) / (gram_len_cnts[len(gram)] - cnt_gram)

    # If any of the probability values are 0 or 1, the likelihood ratio will be either 0 or undefined, and its log will be undefined.
    if not (h0_prob <= 0 or h0_prob >= 1 or h1_prob_t <= 0 or h1_prob_t >= 1 or h1_prob_f <= 0 or h1_prob_f >= 1):
        
        # Calculate the log likelihood ratio.
        # Combinatorial factors in the random variable expressions are nixed.
        log_lambda = -2 * (

            # numerator: likelihood under the null hypothesis

            # log of the probability of the "gram comes before"-class of our observations
            cnt_both * math.log(h0_prob) +
            (cnt_gram - cnt_both) * math.log(1 - h0_prob) +

            # log prob of the "gram does not come before"-class
            (cnt_lett - cnt_both) * math.log(h0_prob) +
            (gram_len_cnts[len(gram)] - cnt_lett - cnt_gram + cnt_both) * math.log(1 - h0_prob) -

            # denomenator: likelihood under the alternative hypothesis

            cnt_both * math.log(h1_prob_t) -
            (cnt_gram - cnt_both) * math.log(1 - h1_prob_t) -

            (cnt_lett - cnt_both) * math.log(h1_prob_f) -
            (gram_len_cnts[len(gram)] - cnt_lett - cnt_gram + cnt_both) * math.log(1 - h1_prob_f)

        )

        return log_lambda
    
    elif h1_prob_t == 1:
        pass # auto-obsorb into word-part (or smoothing?)

    return 0


results_prec = dict()
results_succ = dict()

for gram in gram_cnts:
    for lett in alphabet:
        if gram + lett in gram_cnts:
            results_prec[gram + lett] = log_lam(0, gram, lett)
        if lett + gram in gram_cnts:
            results_succ[lett + gram] = log_lam(1, gram, lett)

#json.dump(sorted(results, key=lambda x: x[1], reverse=True), open("collocations/new_gram_collocations.json", "w"))
#json.dump(sorted(results_backward, key=lambda x: x[1], reverse=True), open("collocations/new_gram_collocations_backward.json", "w"))

json.dump(results_prec, open("collocations/preceding_gram_scores.json", "w"))
json.dump(results_succ, open("collocations/succeeding_gram_scores.json", "w"))

#for i in range(3,7):
#    json.dump(sorted([r for r in results if len(r[0])==i], key=lambda x: x[1], reverse=True), open(str(i) + "-gram_collocations.json", "w"))"""