# -*- coding: utf-8 -*

from PIL import Image
from tqdm import tqdm

from recherche.bloc import Bloc
from recherche.graphe import Graphe
from decoupe import *
import couleur

class Ifs :
	""" Une couche de couleurs représentée par un objet 'ifs'
	Attributs :
	 - parametres : la configuration avec laquelle l'ifs est appliqué
	 - blocs : pour chaque bloc destination : (couleur, source)
	 - couleur : les infos représentant la couleur
	 - source : l'indice du bloc source (après transformations)
	"""

	def __init__(self, param=None) :
		self.parametres = param
		self.blocs = []

	def appliquer(self, image) :
		# Applique l'ifs à l'image (nvdg)
		sources = decouper(self.parametres['taille_petit'] * 2, image)
		[ couleur.normaliser(self.parametres['methode_couleur'], bloc) for bloc in sources ]
		sources = [ Bloc(bloc) for bloc in sources ]

		destinations = []
		for col, s in self.blocs :
			i, transfo = s // 8, s % 8
			destinations.append(sources[i].transformer(transfo).data)
			couleur.reproduire(self.parametres['methode_couleur'], col, destinations[-1])

		return recomposer(self.parametres['taille_petit'], destinations, (len(image[0]), len(image)))


	def chercher(param, image, text = 'Compression') :
		# Retourne l'ifs représentant l'image (nvdg)

		destinations = decouper(param['taille_petit'], image)
		destinations = [ Bloc(bloc) for bloc in destinations ]

		sources = decouper(param['taille_petit']*2, image)
		[ couleur.normaliser(param['methode_couleur'], bloc) for bloc in sources ]
		sources = [ Bloc(bloc) for bloc in sources ]
		sources = [ bloc.transformer(transfo) for bloc in sources for transfo in range(8) ]

		G = Graphe(sources, text + ' (1/2)')
		retour = Ifs(param)
		for i in tqdm(range(len(destinations)), text + ' (2/2)') :
			col = couleur.normaliser(param['methode_couleur'], destinations[i].data)
			s = G.chercher(destinations[i])
			correspondance = (col, s) # couleur, source
			retour.blocs.append(correspondance)
		return retour

class ImageFractale :
	def __init__(self, param = None, dimensions = None) :
		self.parametres = param # Paramètres de compressions
		self.dimensions = dimensions # Dimensions de l'image
		self.couches = [] # Les ifs liés aux différentes couches

	def exporter(self, fichier, iterations=10) :
		image = []
		for couche in self.couches :
			I = np.zeros(self.dimensions, dtype=int)
			for i in tqdm(range(iterations), 'Decompression') :
				I = couche.appliquer(I)
			image.append(I)

		if len(image) == 2 : image = [ image[0], image[0], image[0], image[1] ]
		if len(image) > 1 :
			image = [ [ [ image[i][x][y] for i in range(len(image)) ] for y in range(len(image[0][0])) ] for x in range(len(image[0])) ]
		if len(image) == 1 : image = image[0]

		img = Image.fromarray( np.array(image).astype(np.uint8) )
		img.save(fichier)

	def importer(fichier, param) :
		# Ouvre une image et l'importe au format fractale
		img = Image.open(fichier)
		l, h, p = np.array(img).shape
		retour = ImageFractale(param, (l,h))

		couche = [ np.array(img)[:,:,i] for i in range(3) ]
		couche.append(np.array(img)[:,:,3] if p == 4 else np.zeros((l,h), dtype=int))

		# Identification des couches
		if retour.parametres['couleur'] is None :
			retour.parametres['couleur'] = not np.all(couche[0] == couche[1])
		if retour.parametres['transparence'] is None :
			retour.parametres['transparence'] = not np.all(couche[3] == couche[3][0,0])

		# Recherche des ifs
		if retour.parametres['couleur'] :
			for i in range(3) :
				col = ['Rouge', 'Vert ', 'Bleu ']
				retour.couches.append( Ifs.chercher(param, couche[i], col[i]) )
		else :
			retour.couches.append( Ifs.chercher(retour.parametres, couche[0], 'NVDG ') )
		if retour.parametres['transparence'] :
			retour.couches.append( Ifs.chercher(retour.parametres, couche[3], 'Alpha') )

		return retour
