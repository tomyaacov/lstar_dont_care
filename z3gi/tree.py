import itertools

class Tree(object):
    def __init__(self, counter):
        self.id = next(counter)
        self.counter = counter
        self.children = {}
        self.parent = None

    def __getitem__(self, seq):
        trie = self
        for action in seq:
            if action not in trie.children:
                child = Tree(self.counter)
                child.parent = trie
                trie.children[action] = child
            trie = trie.children[action]
        return trie

    def __iter__(self):
        yield self
        for node in itertools.chain(*map(iter, self.children.values())):
            yield node

    def transitions(self):
        for node in self:
            for action in node.children:
                yield node, action, node.children[action]

    def __str__(self, tabs=0):
        space = "".join(["\t" for _ in range(0, tabs)])
        tree = "(n{0}".format(self.id)
        for action in self.children:
            tree += "\n" + space + " {0} -> {1}".format(action, self.children[action].__str__(tabs=tabs + 1))
        tree += ")"
        return tree

    def path(self):
        seq = []
        node = self
        parent = node.parent
        while parent:
            for action in parent.children:
                if parent.children[action] == node:
                    seq.append(action)
                    break
            node = parent
            parent = node.parent
        seq.reverse()
        return seq
