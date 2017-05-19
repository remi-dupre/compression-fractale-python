from enum import IntEnum

import color.spread as spread
import color.save as save

class representation(IntEnum) :
    save = 0
    spread = 1

def normalize(repr, bloc) :
    if repr is representation.save :
        return save.normalize(bloc)
    elif repr is representation.spread :
        return spread.normalize(bloc)

def reproduce(repr, info, bloc) :
    if repr is representation.save :
        return save.reproduce(info, bloc)
    elif repr is representation.spread :
        return spread.reproduce(info, bloc)
    