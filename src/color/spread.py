import numpy as np


def normalize(bloc) :
    # Normalise les blocs
    # Retourne le couple (color min, color max) permetant de reproduce le bloc d'origine
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
