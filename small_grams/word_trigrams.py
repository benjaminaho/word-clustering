import os, nltk, json

# Derive 1-, 2-, and 3-grams (2- and 3-grams include start and end char) from token.
def trigramize(orgstr):
    ans = [l for l in orgstr]
    altstr = ' ' + orgstr + ' '
    for i in range(1, len(altstr)-1):
        ans.append(altstr[i-1:i+1])
        ans.append(altstr[i-1:i+2])
    ans.append(altstr[-2] + ' ')
    return ans

pattern = r'''(?x) (?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%?'''

# Create dictionary of token : list of trigrams pairs and its inverse.

dictionary = dict()
dictionary_inv = dict()

for textfn in os.listdir(os.getcwd() + "/texts"):
    with open("texts/" + textfn, "r") as textf:
        for token in nltk.regexp_tokenize(textf.read().replace("-", " ").lower(), pattern):
            if token not in dictionary:
                dictionary[token] = trigramize(token)
                for gram in dictionary[token]:#[g for g in dictionary[token] if len(g) > 1]:
                    if gram not in dictionary_inv:
                        dictionary_inv[gram] = [token]
                    else:
                        dictionary_inv[gram].append(token)

# Save dictionaries to file.
json.dump(dictionary, open("dictionary.json", "w"))
json.dump(dictionary_inv, open("dictionary_inverse.json", "w"))