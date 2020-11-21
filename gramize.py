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

alphabet_set = set(" abcdefghijklmnopqrstuvwxyz.")
alphabet = " abcdefghijklmnopqrstuvwxyz."

words_seen = set()
gram_cnts = [[] for _ in range(len(alphabet))] + [0]

#cnt = 0 ###
for textfn in os.listdir(os.getcwd() + "/texts"):
    #cnt += 1
    #if cnt % 30 == 0:
    print(textfn)
    if textfn[0] == ".":
        continue
    with open("texts/" + textfn, "r") as textf:
        #text = "".join([c for c in textf.read().replace("-", " ").lower() if (ord(c) < 123 and ord(c) > 96)])
        #for token in text.split(" "):
        for token in nltk.regexp_tokenize(textf.read().replace("-", " ").lower(), pattern):
            #if token not in words_seen:
            #    words_seen.add(token)
            for gram in gramize(token):
                if set(gram).issubset(alphabet_set):
                    cur = gram_cnts
                    for i in range(len(gram)):
                        try:
                            cur = cur[alphabet.index(gram[i])]
                        except IndexError:
                            for _ in range(len(alphabet)):
                                cur.append([])
                            cur.append(0)
                    try:
                        cur[-1] += 1
                    except IndexError:
                        for _ in range(len(alphabet)):
                            cur.append([])
                        cur.append(1)
                        
                            #cur = [[] for _ in range(len(alphabet))] + [1]

                    #if gram not in gram_cnts:
                    #    gram_cnts[gram] = 1
                    #else:
                    #    gram_cnts[gram] += 1

json.dump(gram_cnts, open("gram_cnts.json", "w"))