from enum import IntEnum


class Encoder :
	"""
	Provides an encoding of the color for a block.

	The encoding only defines a constraint to apply to the block after each iteration.
	"""

	def normalize(block) :
		"""
		Returns information on the block's color.
		Modifies the block on a way it can be found back.
		"""
		return None

	def reproduce(repr, block) :
		"""
		Apply the modification of the color to the block.
		"""
		pass

from color.spread import Spread
from color.save import Save
