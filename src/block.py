import numpy as np

class Block :
	"""
	Represents a part of an image

	:param data:	pixels of the block
	"""

	SIZE = 8		# Size of a block
	comparisons = 0	# A counter of the comparisons between two blocks

	def __init__(self, data=None) :
		"""
		Creates a new block.

		If data is None, the new block has a random content
		"""
		if data is None :
			# Generates a random block
			valeurs = np.random.random((Block.SIZE, Block.SIZE)) * 256
			self.data = np.array(valeurs, dtype=int)
		else :
			self.data = data

	def dist(A, B) :
		"""
		Calculates variency between two blocks
		"""
		n = len(A.data)
		Block.comparisons += 1

		D = A.data - B.data
		return np.sum(D**2) # // n**2 - (np.sum(D)**2 // n**2) ) 

	def transform(self, i) :
		"""
		Returns the block obtained by applying the tranformation of index i
		"""
		ret = self.data[::2,::2].copy()
		if i > 3 :
			ret = np.flipud(ret)
			i -= 4
		ret = np.rot90(ret, i)
		return Block(ret)

	def __add__(self, b) :
		"""Addition élément by élément"""
		return Block(self.data + b.data)
