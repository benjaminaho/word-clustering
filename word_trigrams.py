import os, nltk, json

# Derive 2-, and 3-grams (including start and end char) from token.
def trigramize(orgstr):
    ans = []
    altstr = ' ' + orgstr + ' '
    for i in range(1, len(altstr)-1):
        ans.append(altstr[i-1:i+1])
        ans.append(altstr[i-1:i+2])
    ans.append(altstr[-2] + ' ')
    return ans

pattern = r'''(?x) (?:[A-Z]\.)+ | \w+(?:-\w+)* | \$?\d+(?:\.\d+)?%?'''

# Create dictionary of token : list of trigrams pairs.

dictionary = dict()

for textfn in os.listdir(os.getcwd() + "/texts"):
    with open("texts/" + textfn, "r") as textf:
        for token in nltk.regexp_tokenize(textf.read().lower(), pattern):
            if token not in dictionary:
                dictionary[token] = trigramize(token)

# Save dictionary to file.
json.dump(dictionary, open("dictionary.json", "w"))


#print(dictionary["london"])
#print(dictionary["a"])
#print(dictionary["ask"])