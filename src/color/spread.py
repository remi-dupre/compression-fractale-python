from color import Encoder

import numpy as np


class Spread(Encoder) :
	"""
	Saves the minimum and maximum values of the block
	"""

	def normalize(bloc) :
		min = np.min(bloc)
		max = np.max(bloc)
		bloc -= min
		if min != max :
			bloc *= 255
			bloc //= max - min
		return (min, max)

	def reproduce(info, bloc) :
		min, max = info
		bloc *= max - min
		bloc //= 255
		bloc += min
