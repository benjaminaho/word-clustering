import os, nltk, json

# Derive all grams from token (including final space character)
def gramize(stri):
    stri = stri + " "
    ans = []#[c for c in stri[:-1]]
    for i in range(len(stri)):
        for j in range(len(stri) - i):
            ans.append([stri[j:j+i+1], True if j == 0 else False])
    return ans

#print(gramize("hello"))

pattern = r'''(?x) (?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%?'''

alphabet = "abcdefghijklmnopqrstuvwxyz "

words_seen = set()
gram_cnts = dict()
num_gram_lens = [{l : [0 for _ in range(30)] for l in alphabet} for _ in range(2)]

for textfn in os.listdir(os.getcwd() + "/texts"):
    with open("texts/" + textfn, "r") as textf:
        for token in nltk.regexp_tokenize(textf.read().replace("-", " ").lower(), pattern):
            if token not in words_seen:
                words_seen.add(token)
                for gram, is_start in gramize(token):#[g for g in gram_cnts[token] if len(g) > 1]:
                    if gram[0] in alphabet and gram[-1] in alphabet:
                        if len(gram) > 1:
                            num_gram_lens[0][gram[-1]][len(gram)-2] += 1
                            num_gram_lens[1][gram[0]][len(gram)-2] += 1
                        if gram not in gram_cnts:
                            gram_cnts[gram] = [1, 1 if not is_start else 0]
                        else:
                            gram_cnts[gram][0] += 1
                            if not is_start:
                                gram_cnts[gram][1] += 1

json.dump(gram_cnts, open("gram_cnts.json", "w"))
json.dump(num_gram_lens, open("num_gram_lens.json", "w"))