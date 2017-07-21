# -*- coding: utf-8 -*

from PIL import Image
from tqdm import tqdm

from block import Block
from search.graph import Graph
from cut import *


class Ifs :
    """
    A color layer represented by an IFS

    :params params:        the configuration the IFS is applied with
    :params blocks:        for each destination block : (color, source)
        :params color:    information representing the color
        :params source:    index of the source block (after transformation)
    """

    def __init__(self, params=None) :
        """Creates an empty IFS"""
        self.params = params
        self.blocks = []

    def apply(self, image) :
        """Applies the IFS to a greyscale image"""
        # Builds sources
        sources = cut(self.params['size_small'] * 2, image)
        [self.params['method_color'].normalize(block) for block in sources]
        sources = [Block(block) for block in sources]

        # Apply function to sources
        destinations = []
        for col, s in self.blocks :
            i, transfo = s // 8, s % 8
            destinations.append(sources[i].transform(transfo).data)
            self.params['method_color'].reproduce(col, destinations[-1])

        # Recomposes the image
        return recompose(self.params['size_small'], destinations, (len(image[0]), len(image)))

    def search(params, image, Searcher=Graph) :
        """
        Returns an IFS representing the image.

        :params params:        params for the ifs
        :params image:        the image to compress
        :params Searcher:    the structure used to search matchs
        """
        destinations = cut(params['size_small'], image)
        destinations = [Block(block) for block in destinations]

        # Build blocks
        sources = cut(params['size_small']*2, image)
        [params['method_color'].normalize(block) for block in sources]
        sources = [Block(block) for block in sources]
        sources = [block.transform(transfo) for block in sources for transfo in range(8)]

        G = Searcher(sources)
        ret = Ifs(params)
        for i in range(len(destinations)) :
            col = params['method_color'].normalize(destinations[i].data)
            s = G.search(destinations[i])
            correspondance = (col, s)  # color, source
            ret.blocks.append(correspondance)
        return ret


class FractalImage :
    """
    An image where layers are defined with IFS.

    :attr params:        parameters applied for the IFS
    :attr dimensions:    dimension of the image (width, length)
    :attr layers:        for each layer, an IFS
    """

    def __init__(self, params=None, dimensions=None) :
        self.params = params
        self.dimensions = dimensions
        self.layers = []

    def export(self, iterations=10) :
        """
        Convert the image to a matricial format

        :param iterations:    Number of iterations of the IFS to apply
        :return:            A PIL image
        """
        # Calculates each layer
        image = []
        for layer in self.layers :
            img_res = np.zeros(self.dimensions, dtype=int)
            for i in range(iterations) :
                img_res = layer.apply(img_res)
            image.append(img_res)

        # Reorganise layers
        if len(image) == 2 :
            image = [image[0], image[0], image[0], image[1]]
        if len(image) > 1 :
            image = [[[image[i][x][y] for i in range(len(image))] for y in range(len(image[0][0]))] for x in range(len(image[0]))]
        if len(image) == 1 :
            image = image[0]

        return Image.fromarray(np.array(image).astype(np.uint8))

    def read(file, params, searcher=Graph) :
        """Opens a file and returns a fractal image representing it"""
        img = Image.open(file)
        l, h, p = np.array(img).shape
        ret = FractalImage(params, (l, h))

        layer = [np.array(img)[:, :, i] for i in range(3)]
        layer.append(np.array(img)[:, :, 3] if p == 4 else np.zeros((l, h), dtype=int))

        # Identification of layers
        if ret.params['color'] is None :
            ret.params['color'] = not np.all(layer[0] == layer[1])
        if ret.params['transparency'] is None :
            ret.params['transparency'] = not np.all(layer[3] == layer[3][0, 0])

        # Research of the IFS
        if ret.params['color'] :
            for i in range(3) :
                col = ['Red', 'Green', 'Blue']
                ret.layers.append(Ifs.search(params, layer[i], searcher))
        else :
            print("Greyscale")
            ret.layers.append(Ifs.search(ret.params, layer[0], searcher))
        if ret.params['transparency'] :
            print("Alpha layer")
            ret.layers.append(Ifs.search(ret.params, layer[3], searcher))

        return ret
