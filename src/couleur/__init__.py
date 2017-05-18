from enum import IntEnum

import couleur.etaler as etaler
import couleur.enregistrer as enregistrer

class representation(IntEnum) :
    enregistrer = 0
    etaler = 1

def normaliser(repr, bloc) :
    if repr is representation.enregistrer :
        return enregistrer.normaliser(bloc)
    elif repr is representation.etaler :
        return etaler.normaliser(bloc)

def reproduire(repr, info, bloc) :
    if repr is representation.enregistrer :
        return enregistrer.reproduire(info, bloc)
    elif repr is representation.etaler :
        return etaler.reproduire(info, bloc)