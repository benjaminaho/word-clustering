class Counts():

    def __init__(self, alphabet, tree):
        self.alphabet = alphabet
        self.tree = tree
        self.trees_mem = dict()


    def gram(self, gram):
        return self.gram_leaf(gram)[-1]

    def prev(self, prev, len_gram):
        #try:
        #    return sum(prev_gram_tree[-1] for prev_gram_tree in self.trees_mem[prev][len_gram])
        #except KeyError:
        #    self.trees_mem[prev + str(len_gram)] = [prev_gram_tree for prev_gram_tree in self.sub_trees(self.gram_leaf(prev), len_gram)]
        #    return self.prev(prev, len_gram)
        return sum(prev_gram_tree[-1] for prev_gram_tree, _ in self.sub_trees(len_gram, prev, self.gram_leaf(prev)))

    def post(self, len_gram, post):
        #try:
        #    return sum(self.gram_leaf(post, gram_tree)[-1] for gram_tree in self.trees_mem[str(len_gram)])
        #except KeyError:
        #    self.trees_mem[str(len_gram)] = [gram_tree for gram_tree in self.sub_trees(self.tree, len_gram)]
        #    return self.post(len_gram, post)
        return sum(self.gram_leaf(post, gram_tree)[-1] for gram_tree, _ in self.sub_trees(len_gram))

    def prev_post(self, prev, len_gram, post):
        return sum(self.gram_leaf(post, prev_somegram)[-1] for prev_somegram, _ in self.sub_trees(len_gram, prev, self.gram_leaf(prev)))

    def by_len(self, len_gram):
        return sum(gram_tree[-1] for gram_tree, _ in self.sub_trees(len_gram))


    def gram_leaf(self, gram, root=None):
        cur = root if root is not None else self.tree
        try:
            for l in gram:
                cur = cur[self.alphabet.index(l)]
            #cur[0] # force exception if len(cur) > 0
            return cur if len(cur) > 0 else [0]
        except IndexError:
            return [0]

    def sub_trees(self, length, prev="", root=None):
        root = self.gram_leaf(prev) if root is None else root
        if len(root) > 1:
            if length == 0:
                yield root, prev
            else:
                if prev not in self.trees_mem:
                    self.trees_mem[prev] = []
                try:
                    for leaf, leaf_prev in self.trees_mem[prev][length-1]:
                        yield leaf, leaf_prev
                #except KeyError:
                #    self.trees_mem[prev] = []
                #    for leaf in self.sub_trees(prev, length, root):
                #        yield leaf
                except IndexError:
                    latest_len = len(self.trees_mem[prev])
                    self.trees_mem[prev].extend([[] for _ in range(length-latest_len)])
                    for latest_root, latest_prev in (self.trees_mem[prev][latest_len-1] if latest_len > 0 else [[root, prev]]):
                        for branch_idx in range(len(latest_root)-1):
                            for leaf, leaf_prev in self.sub_trees(length-latest_len-1, latest_prev + self.alphabet[branch_idx], latest_root[branch_idx]):
                                self.trees_mem[prev][length-1].append([leaf, leaf_prev])
                                yield leaf, leaf_prev
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