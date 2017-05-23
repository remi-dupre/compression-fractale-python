from tqdm import *
from random import randint

from search import BlockStruct
from block import Block
import search.trivial as trivial


class Graph(BlockStruct) :
	"""
	Represents a set of blocks with a graph (actualy, a tree)

	:param neighbours: list of adjacency
	:param sources: list of the blocks
	"""

	def __init__(self, sources, members=None, d=100) :
		n = len(sources)

		if members is None :
			members = range(n)

		d = min(d, len(members))

		self.sources = sources
		self.members = members
		self.neighbours = [ [] for i in range(n) ] # Nodes initialy have no neighbour

		# Connect every blocks in the tree
		for i in members :
			parent, _ = self.searchd(sources[i]) # Searches a close block in current graph
			self.neighbours[parent].append(i) # Adds a vertex between both

		# Force graph density
		for i in members[1:] :
			while len(self.neighbours[i]) < d :
				k = randint(0, len(self.members)-1)
				v = self.members[k]
				if not v in self.neighbours[i] :
					self.neighbours[i].append(v)

	def searchd(self, block, node=None, dist=None) :
		"""
		Gives the index of a close block and its distance

		:param block:	the block we try to approximate
		:param node:	(optional) the node the search is starting from
		:param dist:	(optional) the distance between node and block (only specified to avoid one comparison)
		"""
		if not self.members :
			# If the set is empty
			return None, None

		if node is None :
			node = self.members[0]
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

	def search(self, block, node=None, dist=None) :
		"""Workds like ``searchd`` but only returns the block index"""
		s, _ = self.searchd(block, node, dist)
		return s
