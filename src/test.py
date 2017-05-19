# -*- coding: utf-8 -*

import color
import compression
import pickle

params = {
	'size_small' : 8, # la taille des petits blocks
	'method_color' : color.representation.spread,
	'transparency' : None,
	'color' : None
}

img = compression.FractalImage.read('../lenna.png', params)
img.export().save('debug.png')

pickle.dump(img, open("lenna.ifs", "wb"))
