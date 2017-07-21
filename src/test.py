# -*- coding: utf-8 -*

from threading import Thread
from time import sleep, time

import color
import compression
import pickle

from block import Block
from search import methods


def test(searcher) :
    params = {
        'size_small' : 8,
        'method_color' : color.Spread,
        'transparency' : None,
        'color' : None
    }

    img = compression.FractalImage.read('../lenna.png', params, searcher)

    img.export().save("../test/" + searcher.__name__ + "-lenna.png")
    pickle.dump(img, open("../test/" + searcher.__name__ + "-lenna.ifs", "wb"))


for searcher in methods :
    print("##", searcher.__name__)
    Block.comparisons = 0
    t_start = time()

    test(searcher)

    print(" -", Block.comparisons, "comparaison")
    print(" -", int(time()-t_start), "secs")
    print()
