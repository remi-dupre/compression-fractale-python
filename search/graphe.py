from operator import itemgetter
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
		self.sources = []
		self.neighbours = []

		for block in sources :
			self.insert(block)

	def insert(self, block) :
		"""
		Inserts a block in the graph

		To do so, it searches a close block in current graph, and adds a vertex between both
		"""
		n = len(self.sources)
		self.sources.append( block ) # Add the block to node list
		self.neighbours.append( [] ) # The new node has no neighbour

		# If the node is not the first one, adds a new vertex
		if n > 0 :
			parent, _ = self.searchd(block)
			self.neighbours[parent].append(n) # The graph isn't directed


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
		"""Workds like ``searchd`` but only returns the block"""
		s, _ = self.searchd(block, node, dist)
		return self.sources[s]
