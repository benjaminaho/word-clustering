class Counts():

    def __init__(self, alphabet, tree):
        self.alphabet = alphabet
        self.tree = tree


    def gram(self, gram):
        return self.gram_leaf(self.tree, gram)[-1]

    def prev(self, prev, len_gram):
        return sum(prev_gram_tree[-1] for prev_gram_tree in self.sub_trees(self.gram_leaf(self.tree, prev), len_gram))

    def post(self, len_gram, post):
        return sum(self.gram_leaf(gram_tree, post)[-1] for gram_tree in self.sub_trees(self.tree, len_gram))

    def prev_post(self, prev, len_gram, post):
        return sum(self.gram_leaf(prev_somegram, post)[-1] for prev_somegram in self.sub_trees(self.gram_leaf(self.tree, prev), len_gram))

    def by_len(self, len_gram):
        return sum(gram_tree[-1] for gram_tree in self.sub_trees(self.tree, len_gram))


    def gram_leaf(self, root, gram):
        cur = root
        try:
            for l in gram:
                cur = cur[self.alphabet.index(l)]
            return cur if len(cur) > 0 else [0]
        except IndexError:
            return [0]

    def sub_trees(self, root, length, step=0):
        if len(root) > 1:
            if step == length:
                yield root
            else:
                for branch in root[:-1]:
                    for leaf in self.sub_trees(branch, length, step+1):
                        yield leaf
"""
import json

t = Counts(" abcdefghijklmnopqrstuvwxyz.", json.load(open("gram_cnts.json", "r")))
#print(t.count_prev_post("re",2,"able"))
print(t.gram(" red"))
#print(t.prev(" re",2))
#print(t.prev(" re",3))
#print(t.prev(" re",4))
#print(t.prev(" re",5))
#print(t.count_post(4,"w"))"""