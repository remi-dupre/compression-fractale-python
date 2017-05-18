from tqdm import *

from search import BlockStruct
from block import Block
import search.trivial as trivial


class Graph(BlockStruct) :
	"""
	Represents a set of blocks with a graph (actualy, a tree)

	:param neighbours: list of adjacency
	:param sources: list of the blocks
	"""

	def __init__(self, sources) :
		n = len(sources)

		self.sources = sources
		self.neighbours = [ [] for i in range(n) ] # Nodes initialy have no neighbour

		# Connect every blocks in the tree
		for i in range(1, n) :
			parent, _ = self.searchd(sources[i]) # Searches a close block in current graph
			self.neighbours[parent].append(i) # Adds a vertex between both

	def searchd(self, block, node=0, dist=None) :
		"""
		Gives the index of a close block and its distance

		:param block:	the block we try to approximate
		:param node:	(optional) the node the search is starting from
		:param dist:	(optional) the distance between node and block (only specified to avoid one comparison)
		"""
		if dist is None :
			dist = Block.dist(self.sources[node], block)

		if not self.neighbours[node] :
			# Reached a leaf
			return node, dist
		else :
			# Search for closest descendant
			# Redirects research to it if he is closer than current node
			son, son_dist = trivial.search_dist(self.sources, block, self.neighbours[node])
			if son_dist < dist :
				return self.searchd(block, son, son_dist)
			else :
				return node, dist

	def search(self, block, node=0, dist=None) :
		"""Workds like ``searchd`` but only returns the block index"""
		s, _ = self.searchd(block, node, dist)
		return s
