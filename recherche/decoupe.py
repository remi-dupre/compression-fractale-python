from operator import itemgetter

from recherche.bloc import Bloc
import recherche.trivial as trivial


TAILLE_MIN_DECOUPE = 10 # Le nombre de

class Zone :
	# Représente le partitionement d'un ensemble de blocs
	# Attributs :
	#  - (list) sources : liste des blocs sources
	#  - (list) membres : liste des membres de la zone
	#  - (bool) feuille : vrai si la zone n'a pas été redécoupée
	# Si ce n'est pas une feuille :
	#  - (int) centre : l'indice du représentant de la zone
	#  - (float) r1, r2 : les deux rayons délimitant 3 zones
	#  - (Zone) b1, b2, b3 : les trois zones
	
	def __init__(self, sources, membres=None, distances=None) :
		# Crée une zone représentant la liste des membres
		# Distance est défini pour ne pas être recalculé si le centre (premier élément de 'membres') est le même que celui de la zone parente
		if membres is None : membres = range( len(sources) )
		
		self.sources = sources
		self.membres = membres
		self.feuille = len(membres) < TAILLE_MIN_DECOUPE 
		
		if not self.feuille :
			self.centre = membres[0]
			if distances is None :
				distances = [ (bloc, self.eloignement(sources[bloc])) for bloc in membres[1:] ]
				distances.sort(key=itemgetter(1)) # Ordonne par ordre croissant de distance
				self.membres = [ self.centre ] + [ bloc for bloc, _ in distances ] # Réinjecte dans membres

			p1, p2 = len(distances)//3, 2*len(distances)//3 # On coupe à la médiane
			self.r1, self.r2 = distances[p1][1], distances[p2][1]
			
			self.b1 = Zone(sources, self.membres[:p1], distances[:p2])
			self.b2 = Zone(sources, self.membres[p1:p2])
			self.b3 = Zone(sources, self.membres[p2:])
	
	def eloignement(self, bloc) :
		# Retourne l'éloignement du bloc au centre de la zone
		return Bloc.distance(bloc, self.sources[self.centre])
	
	def candidats(self, bloc) :
		# Retourne une liste de potentiels blocs proches de 'bloc'
		if self.feuille :
			return list(self.membres)
		elif self.eloignement(bloc) < self.r1 :
			return self.b1.candidats(bloc) + self.b2.candidats(bloc)
		elif self.eloignement(bloc) > self.r2 :
			return self.b1.candidats(bloc) + self.b2.candidats(bloc) + self.b3.candidats(bloc)
		else :
			return self.b2.candidats(bloc) + self.b3.candidats(bloc)
	
	def chercher(self, bloc) :
		# Recherche un bloc source proche dans la zone, en retoure l'indice
		return trivial.chercher(self.sources, bloc, self.candidats(bloc))
