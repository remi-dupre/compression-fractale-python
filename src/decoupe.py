from math import ceil
import numpy as np

def decouper(taille, image) :
	# Retourne un liste de blocs découpés de l'image (nvdg)
	# Il faut que la taille divise les dimensions de l'image
	retour = []
	l, h = image.shape
	nl, nh = ceil(l/taille), ceil(h/taille)
	for i in range(nl) :
		for j in range(nh) :
			retour.append( image[taille*i:taille*(i+1), taille*j:taille*(j+1)].copy().astype(int) )
	return retour

def recomposer(taille, decoupe, dim) :
	largeur, hauteur = dim
	nb_c = largeur // taille
	nb_l = hauteur // taille
	lignes = [ np.concatenate(decoupe[nb_c*i:nb_c*(i+1)], axis=1) for i in range(nb_l) ]
	return np.concatenate(lignes)
