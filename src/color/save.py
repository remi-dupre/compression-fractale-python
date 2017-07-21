from color import Encoder


class Save(Encoder) :
    """
    Saves the first pixel of the block
    """

    def normalize(block) :
        """The block is represented with its first pixel"""
        return block[0, 0]

    def reproduce(repr, block) :
        """Sets the first pixel of the block"""
        block[0, 0] = repr
