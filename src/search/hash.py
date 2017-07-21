from block import Block
from search import BlockStruct
from search.separate import Zone
from search.graph import Graph


def hash_by_sum(block, threshold=128) :
    """
    A pixel weights in the hash if him or a neighbour is greater to threshold
    """
    n, m = block.data.shape
    ret = 0
    for x in range(n) :
        for y in range(m) :
            over = False
            i = y + (n*x)
            for (a, b) in [(0, -1), (0, 1), (1, 0), (-1, 0), (0, 0)] :
                if x+a in range(n) and y+b in range(m) and block.data[x+a, y+b] > threshold :
                    over = True
            if over :
                ret += 2**i
    return ret % (2**16)


class Hash(BlockStruct) :
    """
    Saves a block in a list, indexed by a hash

    This hash is supposed to caracterize the block in a certain way.
    """
    hash_fun = hash_by_sum

    def __init__(self, blocks, members=None) :
        if members is None :
            members = range(len(blocks))

        self.sources = list(blocks)
        self.members = members
        self.default = Zone(blocks, members)  # Structure used for full search
        self.hashtable = [[] for i in range(2**16)]

        # Places every member in a bukket
        for i in members:
            hash = Hash.hash_fun(blocks[i])
            self.hashtable[hash].append(i)

        # Uses another structure inside the bukket
        for i in range(len(self.hashtable)) :
            self.hashtable[i] = Zone(blocks, self.hashtable[i])

    def search(self, block) :
        """Search the block in the container corresponding to his hash"""
        hash = Hash.hash_fun(block)
        ret = self.hashtable[hash].search(block)
        if ret is None :
            ret = self.default.search(block)
        return ret
