# -*- coding: utf-8 -*

import couleur
import compression
import pickle

parametres = {
	'taille_petit' : 4, # la taille des petits blocs
	'methode_couleur' : couleur.representation.etaler,
	'transparence' : None,
	'couleur' : None
}

img = compression.ImageFractale.importer('lenna.png', parametres)
img.exporter('debug.png')

pickle.dump(img, open("lenna.ifs", "wb"))
