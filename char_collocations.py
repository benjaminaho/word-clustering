"""Find pairs of grams which appear together significantly more often than by chance according to their log likelihood ratio.

This idea came from the usage of the log likelihood ratio for word collocation discovery as
described in Manning and Schütze's Foundations of Statistical Natural Language Processing.

For each gram type (gram 1) in the corpus and a corresponding list of gram types sorted by the
number of word types in which they immediately follow gram 1, iterate through the list determining
if the current gram type (gram 2) forms a collocation with the gram 1. A gram pair is classified as
a collocation if the two constituent grams occur together significantly more often than they would
by chance. In this implementation, this is determined by the log of the ratio of the likelihoods of
the observed occurences of the grams according to two different hypotheses. These are H0: the
probability of gram 1 occuring given that gram 2 occurs next in the word is the same as the
probability that gram 1 occurs given that gram 2 does not occur next (they are independent events),
and H1: these probabilities are different.

If we treat a gram in a word as a Bernoulli trial where success is the occurence of a gram we're
interested in and failure is the occurence of any other gram, we can describe our observations as an
event in the sample space of a binomial random variable. Since we're interested in the occurence of
a gram 1 given the presence or lack thereof of a following gram 2, we split the set of observations
into two classes: those grams which are right before gram 2 in a word, and those which are not. Then
we may express the likelihood of either hypothesis as the product of two binomial random variables:
one representing the probability of the number of occurences of gram 1 in the first class (gram 2
occurs next), and the other representing that in the second class (gram 2 does not occur next). We
divide the liklehoods according to the two hypotheses to obtain a likelihood ratio. The design of
this ratio implies that -2 times its log will be asymptotically chi-squared distributed (Manning &
Schütze 175). With a confidence level of alpha = 0.001, the critical value for one degree of freedom
(the number of parameters in the H1 model less that in the H0 model) is 10.828.

Using a not-carefully constructed corpus of English (several random texts from Project Gutenburg),
this system is able to identify some meaningful word-parts. In each of the four collocation-length
result classes, the six collocations with the highest log likelihood ratio scores are (a space is a
word-start or -end character):

3-letter: " co", " ex", " un", " in", " re", "tio"
4-letter: "atio", " con", " dis", " pro", " com", "ight"
5-letter: " over", " comp", "tatio", " cons", "ratio", " comm"
6-letter: " trans", " inter", " circu", " contr", "abilit", " conve"

Many of these examples, such as " re", " dis", " over", " inter", are cleary common affixes in
English. Other detected word-parts are more semantic than functional, such as " comm", "abilit", and
" conve". Others still are just common patterns in English orthography, such as "tio", "ight", and
"tatio". The first two categories are more interesting for purposes of language modelling.
Clustering and disambiguating these collocations as appropriate, and indeed a more powerful system
of word-part discovery in general ought to be the subject of future work.
"""

import json, math

# Load necessary data.
word_to_grams = json.load(open("dictionary.json", "r")) # used as a list of all words
gram_to_words = json.load(open("dictionary_inverse.json", "r"))
gram_to_grams = json.load(open("following_grams.json", "r"))

# Find number of individual grams of a given length in the set of all word types in the corpus.
# Under our gramification model, each word has len(word) monograms, len(word) + 1 bigrams, and len(word) trigrams.
num_grams = 0
for word in word_to_grams:
    num_grams += len(word_to_grams[word])
num_grams = (num_grams-len(word_to_grams))/3

answers = []

# For each gram in the corpus, find following grams which form a collocation with it.
for gram1 in gram_to_grams:

    # Assign frequency of gram 1 and the probability of gram 1 occuring under the null hypothesis.
    cnt_gram1 = len(gram_to_words[gram1])
    h0_prob = cnt_gram1 / (num_grams + len(word_to_grams)) if len(gram1) == 2 else cnt_gram1 / num_grams    # P(gram 1)

    # Determine if the next gram in the list of grams following gram 1 forms a collocation with gram 1.
    # Since the list is in descending order of frequency, if we cannot reject the null hypothesis for one gram, we will not be able to for all subsequent grams.
    log_lambda = 11
    gram2 = None
    gram_iter = iter(gram_to_grams[gram1])
    while log_lambda > 10.828:

        # Append newly discovered collocation to answer list.
        if gram2 is not None:
            answers.append([gram1 + gram2, log_lambda])

        # Get next gram in list and its cooccurrence frequency with gram 1.
        try:
            gram2, cnt_gram12 = next(gram_iter)
        except StopIteration:
            break

        # Assign number of grams according to the gram length.
        num_grams = num_grams + len(word_to_grams) if len(gram2) == 2 else num_grams

        # Assign frequency of gram 2 and the probabilities of gram 1 occuring under the hypothesis of dependence on gram 2.
        cnt_gram2 = len(gram_to_words[gram2])
        h1_prob_t = cnt_gram12 / cnt_gram2                              # P(gram 1 | gram 2)
        h1_prob_f = (cnt_gram1 - cnt_gram12) / (num_grams - cnt_gram2)  # P(gram 1 | not gram 2)

        # If any of the probability values are 0 or 1, the likelihood ratio will be either 0 or undefined, and its log will be undefined.
        if not (h0_prob <= 0 or h0_prob >= 1 or h1_prob_t <= 0 or h1_prob_t >= 1 or h1_prob_f <= 0 or h1_prob_f >= 1):
            
            # Calculate the log likelihood ratio.
            # Combinatorial factors in the random variable expressions are nixed.
            log_lambda = -2 * (

                # numerator: likelihood under the null hypothesis

                # log of the probability of the "gram 2 is next"-class of our observations
                cnt_gram12 * math.log(h0_prob) +                                            # 1 & 2
                (cnt_gram2 - cnt_gram12) * math.log(1 - h0_prob) +                          # not 1 & 2

                # log prob of the "gram 2 is not next"-class
                (cnt_gram1 - cnt_gram12) * math.log(h0_prob) +                              # 1 & not 2
                (num_grams - cnt_gram1 - cnt_gram2 + cnt_gram12) * math.log(1 - h0_prob) -  # not 1 & not 2

                # denomenator: likelihood under the alternative hypothesis

                # log prob of the "gram 2 is next"-class
                cnt_gram12 * math.log(h1_prob_t) -
                (cnt_gram2 - cnt_gram12) * math.log(1 - h1_prob_t) -

                # log prob of the "gram 2 is not next"-class
                (cnt_gram1 - cnt_gram12) * math.log(h1_prob_f) -
                (num_grams - cnt_gram1 - cnt_gram2 + cnt_gram12) * math.log(1 - h1_prob_f)

            )
        
        # Reassign number of grams to default value.
        num_grams = num_grams - len(word_to_grams) if len(gram2) == 2 else num_grams

# Save answers according to their collocation-lengths.
for i in range(3,7):
    json.dump(sorted([ans for ans in answers if len(ans[0])==i], key=lambda x: x[1], reverse=True), open("collocations/" + str(i) + "-gram_collocations.json", "w"))