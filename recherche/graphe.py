from operator import itemgetter
from tqdm import *

from recherche.bloc import Bloc
import recherche.trivial as trivial

class Graphe :
	# Représente un ensemble de Blocs par un graphe
	# Attributs :
	#  - voisins : liste des listes d'adjacence
	#  - sources : liste des blocs source
	# La racine de l'arbre est le bloc d'indice 0

	def __init__(self, sources, texte='Compression') :
		# Initialise le graphe
		# Entrée (sources) : la liste des blocs à représenter

		n= len(sources)
		self.sources = sources
		self.voisins = [ [] for _ in range(n) ]

		distances = [ (Bloc.distance(sources[i], sources[0]), i) for i in range(1, len(sources)) ]
		# distances.sort(key=itemgetter(0)) # On ajoute les blocs par ordre croissant de distance
		for dist, i in tqdm(distances, texte) :
			parent, dist = self.chercherd(sources[i])
			if dist > 0 :
				self.voisins[parent].append(i)


	def chercherd(self, bloc, sommet=0, dist=None) :
		# Retourne l'indice d'un bloc proche dans le graphe et sa distance
		# Entrées :
		#  - bloc : le bloc qu'on cherche à approcher
		#  - sommet : le sommet d'où part la recherche
		#  - dist : la distance du bloc à ce sommet

		if dist is None : dist = Bloc.distance(self.sources[sommet], bloc)
		if not self.voisins[sommet] :
			return sommet, dist
		else : # On cherche si un descendant du sommet est plus proche
			fils, nv_dist = trivial.chercher_min(self.sources, bloc, self.voisins[sommet])
			if nv_dist < dist :
				return self.chercherd(bloc, fils, nv_dist)
			else :
				return sommet, dist

	def chercher(self, bloc, sommet=0, dist=None) :
		# Retourne l'indice d'un bloc proche dans le graphe
		# Entrées :
		#  - bloc : le bloc qu'on cherche à approcher
		#  - sommet : le sommet d'où part la recherche
		#  - dist : la distance du bloc à ce sommet

		s, _ = self.chercherd(bloc, sommet, dist)
		return s
