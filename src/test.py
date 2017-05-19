# -*- coding: utf-8 -*

from threading import Thread
from time import sleep

import color
import compression
import pickle

from search import methods


def test(searcher) :
	params = {
		'size_small' : 4, # la taille des petits blocks
		'method_color' : color.Spread,
		'transparency' : None,
		'color' : None
	}

	img = compression.FractalImage.read('../lenna.png', params, searcher)

	img.export().save("../test/" + searcher.__name__ + "-lenna.png")
	pickle.dump(img, open("../test/" + searcher.__name__ + "-lenna.ifs", "wb"))

for searcher in methods :
	test(searcher)