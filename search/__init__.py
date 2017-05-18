"""
Different implementations of structures to find a closest block

 - trivial.py	: processes an exhaustive research
 - graphe.py	: builds recursively a graph, adding a vertex with a closest node
 - decoupe.py	: builds a graph, where space is divided in 3, depending on the distance with the node
"""

from abc import ABCMeta, abstractmethod

class BlockStruct(metaclass=ABCMeta) :
	"""
	Structure storing a set of blocks
	
	This structure has to cover these functionnalities :
	 - insertion in the structure
	 - searching for the closest block to a given block (at least an approximation)
	"""

	@abstractmethod
	def __init__(self, blocks) :
		"""Creates a new structure with initial content ``blocks``, a list of blocks"""
		...

	@abstractmethod
	def insert(self, block) :
		"""Inserts a new block in the structure"""
		...

	@abstractmethod
	def search(self, block) :
		"""Search a block in the structure, supposed to be close from ``block``"""
		...
