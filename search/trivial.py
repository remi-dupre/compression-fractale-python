"""Methods for exaustive research"""

from block import Block
from search import BlockStruct


def search_dist(sources, block, members=None) :
	"""
	Returns closest block
	
	:param sources:	list of blocks that could be returned
	:param block:	the block that must be appoximated
	:param members:	(optional) indices to consider in 'sources'

	:return: a tuple containing the index of closest block, and the distance between both
	"""

	if members is None :
		members = range(len(sources))
	
	min_dist = float('inf')
	min_block = None
	for s in members :
		dist = Block.dist(sources[s], block)
		if dist < min_dist :
			min_dist = dist
			min_block = s
	return min_block, min_dist

def search(sources, bloc, members=None) :
	"""Same as search_dist but doesn't return the distance"""
	r, _ = search_dist(sources, bloc, members)
	return r


class Exaustive(BlockStruct) :
	"""
	Keeps all the blocks in a list
	Makes an exhaustive search in it to find the closest
	"""

	def __init__(self, blocks) :
		# block has to be an iterable of blocks
		self.blocks = list(blocks) # Only has to store the block list

	def insert(self, block) :
		self.blocks.append(block)

	def search(self, block) :
		i = search(self.blocks, block)
		return self.blocks[i]
