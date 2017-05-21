"""
Different implementations of structures to find a closest block

 - trivial.py	: processes an exhaustive research
 - graph.py		: builds recursively a graph, adding a vertex with a closest node
 - separate.py	: builds a graph, where space is divided in 3, depending on the distance with the node
"""

from abc import ABCMeta, abstractmethod


class BlockStruct(metaclass=ABCMeta) :
	"""
	Structure storing a set of blocks
	
	This structure has to cover these functionnalities :
	 - build the structure from scratch
	 - searching for the closest block to a given block (at least an approximation)
	"""

	@abstractmethod
	def __init__(self, blocks) :
		"""Creates a new structure with initial content ``blocks``, a list of blocks"""
		...

	@abstractmethod
	def search(self, block) :
		"""Search a block in the structure, supposed to be close from ``block``"""
		...


# The differents classes that can store blocks
from search.hash import Hash
from search.graph import Graph
from search.separate import Zone
from search.trivial import Exaustive

methods = [Hash, Graph, Zone, Exaustive]

# To make random tests
from search.compare import test_random
