from math import ceil
import numpy as np

def cut(size, image) :
	"""
	Cuts the image in same-sized blocks

	:paramseter size:	width of the squares the pic is divided in
	:paramseter image:	the image that must be cut

	.. warning:: the size must divide both dimentions of the image
	"""
	ret = []
	l, h = image.shape
	nl, nh = ceil(l/size), ceil(h/size)
	for i in range(nl) :
		for j in range(nh) :
			ret.append(
				image[size*i:size*(i+1), size*j:size*(j+1)].copy().astype(int)
			)
	return ret

def recompose(size, cut, dim) :
	"""
	Rebuilds a cutted image

	:paramseter size:	the size of the base squares
	:paramseter cut:		the list of all blocks
	:paramseter dim:		tuple containing the dimention of the image
	"""
	# Calculates the number of lines and columns of the division
	width, height = dim
	nb_c = width // size
	nb_l = height // size

	# Concatenates the divisions
	lines = [ np.concatenate(cut[nb_c*i:nb_c*(i+1)], axis=1) for i in range(nb_l) ]
	return np.concatenate(lines)
