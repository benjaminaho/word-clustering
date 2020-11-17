import os, nltk, json

word_to_grams = dict()

# Derive all grams from token (including final space character)
def gramize(stri):
    global word_to_grams
    if stri in word_to_grams:
        return word_to_grams[stri]
    
    stri = " " + stri + "."
    ans = []#[c for c in stri[:-1]]
    for i in range(len(stri)):
        for j in range(len(stri) - i):
            ans.append(stri[j:j+i+1])

    word_to_grams[stri] = ans
    return ans

#print(gramize("hello"))

pattern = r'''(?x) (?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%?'''

alphabet = set(" abcdefghijklmnopqrstuvwxyz.")

words_seen = set()
gram_cnts = dict()

cnt = 0 ###
for textfn in os.listdir(os.getcwd() + "/texts"):
    cnt += 1
    if cnt % 30 == 0:
        print(textfn, cnt/30)
    if textfn[0] == ".":
        continue
    with open("texts/" + textfn, "r") as textf:
        text = "".join([c for c in textf.read().replace("-", " ").lower() if (ord(c) < 123 and ord(c) > 96)])
        for token in text.split(" "):
            #if token not in words_seen:
            #    words_seen.add(token)
            for gram in gramize(token):
                if set(gram).issubset(alphabet):
                    if gram not in gram_cnts:
                        gram_cnts[gram] = 1
                    else:
                        gram_cnts[gram] += 1

json.dump(gram_cnts, open("gram_cnts.json", "w"))