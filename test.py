# -*- coding: utf-8 -*

import couleur
import compression

parametres = {
    'taille_petit' : 4, # la taille des petits blocs
    'methode_couleur' : couleur.representation.etaler,
    'transparence' : None,
    'couleur' : None
}

img = compression.ImageFractale.importer('Lenna.png', parametres)
img.exporter('debug.png')
